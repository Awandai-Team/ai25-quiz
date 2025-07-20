# ai25-quiz: Awandai Team

Team: Awandai  ( @tawanNophaket , @Dai5onda , @chayapan )

การแข่งขัน Hackathon 2025: From AI Model to Service on AI FOR THAI
https://aift.hackathon2025.ai.in.th/

Solution: Quiz

วิธีการทดสอบ
1. รัน Docker Compose ระบบจะสร้างคอนเทนเนอร์
2.

## Deploy

Start API service.

```
docker-compose up -d
docker ps
```

| Service                | Port | Description             |
|------------------------|------|-------------------------|
| API 1                  | 8001 | Backend API service     |
| API 2                  | 8002 | Backend API service     |
| Web / Middleware       | 80xx | Web server or gateway   |
| Caching / Front-end    |      | Cache layer or frontend |
| RDBMS / Persistent-Layer |    | Database service        |


### Example/Endpoint

Docker Compose deployment provides following endpoints:

* API1
** localhost:8001/v1/foo
** localhost:8001/v1/bar
** localhost:8001/v1/call-api2
* API2
** localhost:8002/docs
** localhost:8002/health
** localhost:8002/v1/chat-response

# Test

To test this deployment.

```
docker-compose up -d
docker-compose ps
pytest
```


## API 1

* Go (and Flask) reference implementation. Request to this HTTP endpoint is logged to [logs/api1.log]()


```
cd api1/
```

Flask

```
python3 app.py
```


Go

```
go run main.go
```


## API 2

* FastAPI reference implementation. Request to this HTTP endpoint is logged to [logs/api2.log]()


```
python3 -m pip install fastapi[standard]
uvicorn main:app --reload --host "0.0.0.0" --port "8000"
```


# Logging

There are seven log files in this solution prototype.

```
logs/
  client.log
  web.log
  task.log
  job.log
  db.log
  inference.log
  hourly.log
```

# Web

1. Run Terminal: docker-compose up --build -d
2. Go to Browser: http://localhost:8080

