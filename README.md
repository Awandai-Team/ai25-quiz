# ai25-quiz: Awandai Team

Team: Awandai
Problem: Quiz

การแข่งขัน Hackathon 2025: From AI Model to Service on AI FOR THAI
https://aift.hackathon2025.ai.in.th/

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
| Web / Middleware       | 8080 | Web server or gateway   |
| Caching / Front-end    |      | Cache layer or frontend |
| RDBMS / Persistent-Layer |    | Database service        |


TODO:

How-to Test ...


## API 1

* Go or Flask. This solution provides Go and Flask reference implementation. Request from HTTP is logged to [logs/api1.log]()


```
cd api1
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

```
python3 -m pip install fastapi[standard]
```

Documentation at http://127.0.0.1:8002/docs



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

The web layer. Node.js or Django or PHP. This provides user session to interact with the service.


[//]: # # Console
[//]: # ![[AWS Cloud Shell](https://aws.amazon.com/cloudshell/faqs/#topic-1){:target="_blank"}](https://avatars.githubusercontent.com/u/2232217?s=200&v=4)  ![Google Cloud Platform](https://avatars.githubusercontent.com/u/2810941?s=200&v=4){:target="_blank"}  [//]: # ![Azure Bastion](https://uhf.microsoft.com/images/microsoft/RE1Mu3b.png){:target="_blank"} 
[//]: # https://cloud.google.com/free  
[//]: # https://aws.amazon.com/free/  
[//]: # https://azure.microsoft.com/en-us/products/azure-bastion  


