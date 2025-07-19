# Development Note


## Go installation on development machine

```
go version
go version go1.15.7 darwin/amd64
```


## Middleware Recipe

https://gowebexamples.com/basic-middleware/


## Simple Middleware

```
go run main.go
```

Test 1:
```
curl 127.0.0.1:8001/v1
404 page not found
```

Test 2:
```
curl 127.0.0.1:8001/v1/foo
foo
```

Test 3:
```
curl http://localhost:8001/v1/call-api2
{
    "api1_message": "Hello from API1 (Go)",
    "api2_response": {"Hello": "World"},
    "timestamp": "2024-01-15T10:30:45Z"
}
```

## Add Logging

```
go get gopkg.in/natefinch/lumberjack.v2
```
