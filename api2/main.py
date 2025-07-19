from fastapi import FastAPI
import logging

app = FastAPI()  # สร้างเเอปฟลิเคชัน FastAPI

# Config เเสดงผล Log เป็นระดับ INFO (ข้อมูลทั่วไป)
# จัด format (ดึง เวลา, ชื่อระดับ, ข้อความหลัก)
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - API2 - %(levelname)s - %(message)s"
)


@app.get("/health")  # สร้าง endpoint ไปที่ path "/health"
def read_root():

    # เมื่อมี Request มาที่ endpoint นี้ จะทำงาน
    logging.info(
        "Request received. Sending response."
    )  # Log เพื่อยืนยัน Status ว่า service นี้ถูกเรียกเเล้ว

    # ส่ง JSON response
    return {"message": "Hello from API2", "status": "ok"}
