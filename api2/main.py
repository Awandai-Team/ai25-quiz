import logging
import os
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOG_DIR = "logs"
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

log_formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

log_file = os.path.join(LOG_DIR, "api2.log")

file_handler = RotatingFileHandler(log_file, maxBytes=1024 * 1024 * 5, backupCount=5)
file_handler.setFormatter(log_formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Handler เเบบหมุนเวียน (กันไฟล์เกิน)
handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)

# จัด Format
formatter = logging.Formatter("%(asctime)s - API2 - %(levelname)s - %(message)s")

# กำหนด Format ให้ Handler
handler.setFormatter(formatter)

# เพิ่ม Handler เข้า Logger
logger.addHandler(handler)

""" **** สร้าง FastAPI App ****"""

app = FastAPI()  # สร้างเเอปฟลิเคชัน FastAPI

class Payload(BaseModel):
    question: str
    age: int
    genre: str
    seats: int


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
