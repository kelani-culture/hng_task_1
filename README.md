# Basic API setup


```
https://violent-fifine-hng-ae225d70.koyeb.app/
```

the endpoint above is a simple **GET** request that takes in a query parameter ***visitor_name***  and returns the following response

```
visitor_name: str
```

### request
```
https://violent-fifine-hng-ae225d70.koyeb.app/api/hello?visitor_name=mark
```

#### response
```
{
  "client_ip": "127.0.0.1", // The IP address of the requester
  "location": "New York" // The city of the requester
  "greeting": "Hello, Mark!, the temperature is 11 degrees Celcius in New York"
}
```