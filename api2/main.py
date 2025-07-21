import logging
import os
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime

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


origins = [
    "http://localhost:8080",
    "http://127.0.0.1:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Payload(BaseModel):
    question: str
    age: int
    genre: str
    seats: int


@app.get("/v1/chat-response")
def chat_response_txt(): 
    logger.info("Request received.")
    return {1: 1}


@app.get("/v1/data")
async def get_data():
    logger.info("Received request at /v1/data endpoint")
    return {"message": "Hello from API2", "timestamp": datetime.now().isoformat()}


@app.get("/logs")
async def get_logs():
    try:
        with open(log_file, "r") as f:
            logs = f.readlines()
        return {"logs": [log.strip() for log in logs]}
    except Exception as e:
        logger.error(f"Error reading logs: {e}")
        return {"logs": []}


@app.delete("/logs")
async def clear_logs():
    try:
        with open(log_file, "w") as f:
            f.write("")
        logger.info("Log file cleared successfully")
        return {"message": "Logs cleared"}
    except Exception as e:
        logger.error(f"Error clearing logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")  # สร้าง endpoint ไปที่ path "/health"
def check_status():
    # สั่งให้บันทึก Log
    logger.info("Request received. Sending response.")

    # ส่ง JSON response
    return {"message": "Hello from API2", "status": "ok"}
