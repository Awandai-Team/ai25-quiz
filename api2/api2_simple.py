# Simple API: API2
# - synchronous and async/wait
# - proxy to A.I. model like LLM, Transformers, and DNN
from typing import Union
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

"""
Within the container:

python
>>> res = requests.get("http://localhost:8000")
>>> res.status_code
200
>>> res.content
b'{"Hello":"World"}'

"""
