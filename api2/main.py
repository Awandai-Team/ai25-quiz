"""
================================================================================
 Component API2 - Service API1's request
================================================================================

 Description:
 ------------
 Uses AIFT library and GPT2 for content generation.

Responsibilities:
 -----------------
 - Provide movie recommendation service
 - Provide showtime schedule

 Usage:
 ------
 Run this component as part of a FastAPI server or include in a larger system.

"""
from fastapi import FastAPI
import logging
import os
from pydantic import BaseModel
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

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
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(file_handler)
console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    logger.info("API 2: Root endpoint '/' was called.")
    return {"message": "Hello from API 2"}


@app.get("/v1/data")
def get_data(request: Request):
    client_host = request.client.host
    logger.info(f"API 2: Received request for /v1/data from {client_host}")
    response_data = {"source": "API 2", "data": "This is the data you requested."}
    logger.info(f"API 2: Sending response: {response_data}")
    return response_data

class Payload(BaseModel):
    name: str

@app.get("/v1/chat-response")
def chat_response_txt(): # provides A.I.
    logger.info("Request received.")
    return {1:1}

@app.get("/logs")
def get_logs():
    logger.info("API 2: Log file requested.")
    try:
        if os.path.exists(log_file):
            with open(log_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                if not lines:
                    return {"logs": []}
                return {"logs": [line.strip() for line in lines[-50:]]}
        else:
            return {"logs": []}
    except Exception as e:
        logger.error(f"Could not read log file: {e}")
        return JSONResponse(
            status_code=500, content={"error": "Could not read log file."}
        )

@app.delete("/logs", status_code=204)
def clear_logs():
    try:
        with open(log_file, "w"):
            pass
        logger.info("API 2: Log file cleared successfully.")
    except Exception as e:
        logger.error(f"Could not clear log file: {e}")
        raise HTTPException(status_code=500, detail="Could not clear log file.")
