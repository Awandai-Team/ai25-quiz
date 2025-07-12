# ai25-quiz: Awandai Team

| Service                | Port | Description             |
|------------------------|------|-------------------------|
| API 1                  | 8001 | Backend API service     |
| API 2                  | 8002 | Backend API service     |
| Web / Middleware       | 8080 | Web server or gateway   |
| Caching / Front-end    |      | Cache layer or frontend |
| RDBMS / Persistent-Layer |    | Database service        |


Start API service.

```
docker-compose up -d
docker ps
```


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


## Web

The web layer. Node.js or Django or PHP. This provides user session to interact with the service.

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

# About

การแข่งขัน Hackathon 2025: From AI Model to Service on AI FOR THAI
https://aift.hackathon2025.ai.in.th/


Checklist per quiz  
https://docs.google.com/document/d/14XtBFMgx39MWxpmtZ9_s5qtfIMzIz8ezCy6Wqeurt4Y/edit?tab=t.0

Question/Task:

  [/ ] จงสร้าง API 2 ตัว  โดยมีเงื่อนไขดังนี้
  [/ ] สร้างโดยภาษาไดก็ได้
  [/ ] Listen ที่ port ไดก็ได้
  [ ] User Request ไปที่ API1 แล้ว API 1 request ต่อไปที่ API2 แล้วนำคำตอบส่งกลับไปที่ User
  [ ] มีการ Print logs ทั้งบน API1 และ 2
  [ ] endpoint ของ  api และคำตอบ จะเป็นอะไรก็ได้ แค่ print hello world ก็ได้
  [/ ] deploy ทุกอย่างบน docker-compose.yml
  [/ ] ส่งงานผ่าน github หรือ gitlab เปิด public access
  [? ] เขียน Readme.md บอกวิธี  deploy และทดสอบ
