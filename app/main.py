import json
from typing import Optional

import requests
from fastapi import FastAPI, Request
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

app = FastAPI()


class Person(BaseModel):
    client_ip: str
    location: str
    greeting: str


class Setting(BaseSettings):
    weather_api_key: str

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )


async def get_ip() -> str:
    response = requests.get("https://api.ipify.org")

    if response.status_code != 200:
        return ""
    return response.text


async def get_location(ip_address: str) -> dict:
    location: requests = requests.get(f"https://ipapi.co/{ip_address}/json/")
    if location.status_code != 200:
        return {}
    return location.json()


async def get_weather(location: dict) -> dict:
    API_KEY = Setting().weather_api_key
    query = {
        "lat": location.get("latitude"),
        "lon": location.get("longitude"),
        "appid": API_KEY,
        "units": "metric",
    }
    url = "https://api.openweathermap.org/data/3.0/onecall"
    response = requests.get(url, params=query)
    if response.status_code != 200:
        return {}

    deg = response.json()
    return deg


@app.get("/api/hello")
async def greeting(request: Request, visitor_name: str) ->  Person:
    """
    return a vistor name with greetings
    """
    # get client ip
    client_ip = await get_ip()

    #get info on location
    data_location = await get_location(client_ip)
    state = data_location.get('city')

    # get weather info
    weather_info = await get_weather(data_location)
    deg = weather_info.get('current', {}).get('temp', {})
    greeting: str = (
        f"Hello, {visitor_name}!, the temperature is {deg} degrees Celcius in {state}"
    )

    data = {'client_ip': client_ip, 'location': state, 'greeting': greeting}
    person = Person(**data)
    return person
