# **ai25-quiz: Awandai Team**

|              |                                                      |
| ------------ | ---------------------------------------------------- |
| **Team**     | `Awandai` ( @tawanNophaket , @Dai5onda , @chayapan ) |
| **Solution** | Microservices Application for Hackathon 2025         |

---

## **About This Project**

สร้างระบบที่ประกอบด้วย API สองตัวซึ่งสื่อสารระหว่างกัน และสามารถ Deploy ได้ผ่าน Docker Compose

นอกเหนือจากข้อกำหนดหลัก เราได้สร้าง Frontend เพื่อใช้สาธิตการทำงานของระบบ และแสดงผล Log การทำงานแบบ Real-time ซึ่งช่วยให้เห็นภาพการทำงานของสถาปัตยกรรมที่ออกแบบไว้ได้ชัดเจนขึ้น

---

## **System Architecture**

โซลูชันนี้ใช้สถาปัตยกรรมแบบ Microservices เพื่อแบ่งส่วนการทำงานและเพิ่มความสะดวกในการจัดการ โดยระบบประกอบด้วย 3 Service หลักที่ทำงานใน Docker Container

**Workflow:** `Frontend (User)` ➔ `API 1 (Gateway)` ➔ `API 2 (Backend)`

| Service             | Technology       | Port (Host) | Description                                             |
| ------------------- | ---------------- | ----------- | ------------------------------------------------------- |
| **Frontend**        | Nginx + HTML/JS  | `8080`      | Web Interface สำหรับการทดสอบและแสดงผล Log การทำงาน      |
| **API 1 (Gateway)** | Go               | `8001`      | API Gateway ทำหน้าที่รับ Request และส่งต่อไปยัง Backend |
| **API 2 (Backend)** | Python (FastAPI) | `8002`      | Backend Service สำหรับจัดการ Logic หลักของแอปพลิเคชัน   |

---

## **How to Run and Test**

### **Prerequisites**

- Git
- Docker & Docker Compose

---

### **Step 1: Run the Application**

Clone a repository และใช้ Docker Compose เพื่อ build และ run a service

```bash
# 1. Clone the repository
git clone https://github.com/Awandai-Team/ai25-quiz.git

# 2. Navigate to the project directory
cd ai25-quiz

# 3. Build and run services in detached mode
docker-compose up --build -d
```

**หมายเหตุ**: เปิด `Docker Desktop` ตอนรัน `docker-compose up --build -d`

`docker-compose down`

`docker-compose up -d`

---

### **Step 2: Verify the Services**

ตรวจสอบสถานะของ Container ที่กำลังทำงาน

```bash
docker-compose ps
```

Service ทั้งหมด (`frontend`, `api1`, `api2`) ควรมีสถานะเป็น `up`

---

### **Step 3: Access the Services**

- **Web Interface:** [http://localhost:8080](http://localhost:8080)
- **API Documentation (Swagger UI):** [http://localhost:8002/docs](http://localhost:8002/docs)

---

### **Step 4: Run Tests**

โปรเจกต์มีชุดการทดสอบสำหรับ API 2 โดยใช้ `pytest` สามารถรันได้ด้วยคำสั่ง:

```bash
docker-compose exec api2 pytest
```

**หมายเหตุ**: Test case ส่วนใหญ่ถูกทำเครื่องหมาย `@pytest.mark.skip` ไว้ เนื่องจากเป็นส่วนของฟังก์ชันที่วางแผนไว้สำหรับการพัฒนาในอนาคต

---

### **API Endpoint Reference**

#### **API 1 (Gateway)**

- `GET /v1/call-api2`: Endpoint สำหรับทดสอบ Flow การเรียกไปยัง API 2
- `GET /logs`: เรียกดู Log ของ `api1`
- `DELETE /logs`: ล้างข้อมูลในไฟล์ Log ของ `api1`

#### **API 2 (Backend)**

- `GET /v1/data`: Endpoint ที่ API 1 เรียกใช้
- `GET /health`: Health check สำหรับ `api2`
- `GET /logs`: เรียกดู Log ของ `api2`
- `DELETE /logs`: ล้างข้อมูลในไฟล์ Log ของ `api2`

---

### **Logging**

API แต่ละตัวจะบันทึก Log การทำงานลงในไฟล์ของตัวเองภายใต้ไดเรกทอรี `logs/` ซึ่งจะถูกสร้างขึ้นโดยอัตโนมัติ:

- `logs/api1.log`
- `logs/api2.log`

นอกจากนี้ยังสามารถดู Log แบบ Real-time ได้ที่ Web Interface

---

### **Local Development (Without Docker)**

หากต้องการรันแต่ละ Service แยกกันเพื่อการพัฒนา สามารถทำได้ดังนี้:

#### **API 1 (Go)**

```bash
cd api1/
go run main.go
```

#### **API 2 (Python/FastAPI)**

```bash
cd api2/
pip install -r requirements.txt
uvicorn main:app --reload --host "0.0.0.0" --port "8002"
```

---
