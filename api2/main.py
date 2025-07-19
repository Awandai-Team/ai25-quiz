"""
================================================================================
 Component API2 - Service API1's request
================================================================================

 Description:
 ------------

Responsibilities:
 -----------------
 - Define data models using Pydantic for strict validation and serialization.
 - Expose a RESTful HTTP endpoint to send structured payloads.
 - Act as a transport client to API2, sending validated data over HTTP or gRPC.

 Usage:
 ------
 Run this component as part of a FastAPI server or include in a larger system.

"""
from fastapi import FastAPI
import logging
import os
from pydantic import BaseModel
from logging.handlers import RotatingFileHandler

""" **** ตั้งค่า Logger ****"""

log_file_path = "../logs/api2.log"

# Logger Instance
logger = logging.getLogger("api2_logger")
logger.setLevel(logging.INFO)

# Handler เเบบหมุนเวียน (กันไฟล์เกิน)
handler = RotatingFileHandler(log_file_path, maxBytes=2000, backupCount=5)

# จัด Format
formatter = logging.Formatter("%(asctime)s - API2 - %(levelname)s - %(message)s")

# กำหนด Format ให้ Handler
handler.setFormatter(formatter)

# เพิ่ม Handler เข้า Logger
logger.addHandler(handler)

""" **** สร้าง FastAPI App ****"""

app = FastAPI()  # สร้างเเอปฟลิเคชัน FastAPI

class Payload(BaseModel):
    name: str

@app.get("/v1/chat-response")
def chat_response_txt(): # provides A.I.
    logger.info("Request received.")
    return {1:1}

@app.get("/health")  # สร้าง endpoint ไปที่ path "/health"
def check_status():

    # สั่งให้บันทึก Log
    logger.info("Request received. Sending response.")

    # ส่ง JSON response
    return {"message": "Hello from API2", "status": "ok"}
