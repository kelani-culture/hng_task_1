import json
from typing import Optional
import os
import geocoder
import requests
from fastapi import FastAPI, Request

from pydantic import BaseModel
from dotenv import load_dotenv
load_dotenv()


app = FastAPI()


class Person(BaseModel):
    client_ip: Optional[str]
    location: Optional[str]
    greeting: Optional[str]


async def get_ip() -> str:
    response = requests.get("https://api.ipify.org")

    if response.status_code != 200:
        return ""
    return response.text


# async def get_location(ip_address: str) -> dict:
#     location: requests = requests.get(f"https://ipapi.co/{ip_address}/json/")
#     if location.status_code != 200:
#         return {}
#     return location.json()


async def get_weather(location: str) -> dict:
    API_KEY = os.getenv('WEATHER_API_KEY')
    query = {"key": API_KEY, "q": location, "qi": "no"}
    url = "https://api.weatherapi.com/v1/current.json"
    response = requests.get(url, params=query)
    if response.status_code != 200:
        return {}

    deg = response.json()
    return deg


@app.get("/api/hello")
async def greeting(request: Request, visitor_name: str):
    """
    return a vistor name with greetings
    """
    client_ip = request.client.host
    x_forwarded_for = request.headers.get("x-forwarderd-for")
    if x_forwarded_for:
        client_ip = x_forwarded_for.split(",")[0].strip()

    # get info on location
    client_ip =  await get_ip()
    g = geocoder.ipinfo(client_ip)

    if not g.ok:
        return g

    data_location = g.city
    weather_info = await get_weather(data_location)
    deg = weather_info.get('current', {}).get('temp_c', {})
    greeting: str = (
        f"Hello, {visitor_name}!, the temperature is {deg} degrees Celcius in {data_location}"
    )
    data = {
        "client_ip": client_ip,
        "location": data_location,
        "greeting": greeting,
    }

    if None in data.values():
        return {}, 400
    person = Person(**data)
    return person
