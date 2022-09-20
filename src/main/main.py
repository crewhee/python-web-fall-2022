from asyncore import socket_map
from lib2to3.pytree import Base
from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel


class RequestBody(BaseModel):
    name: str
    description: Union[str, None] = None
    some_number: Union[int, None] = None


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/hello/{name}")
def read_hello(name: str, q: Union[str, None] = None):
    return {"Name": name, "Message": "Hello, " + name}


@app.post("/post_method")
def post_with_body(request: RequestBody):
    return {"Name": request.name,
        "Description": request.description,
        "Square": 0 if request.some_number is None else request.some_number ** 2
        }