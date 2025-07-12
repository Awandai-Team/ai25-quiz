from fastapi import FastAPI
import asyncio

app = FastAPI()

@app.get("/")
async def read_root():
    await asyncio.sleep(1)  # Simulates an async I/O operation
    return {"message": "Hello, Async World!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int, delay: int = 2):
    await asyncio.sleep(delay)  # Simulate I/O delay
    return {"item_id": item_id, "status": f"delayed for {delay} seconds"}
