from fastapi import APIRouter
from typing import Union
from ..models.request_models import RequestBody

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/hello/{name}")
def read_hello(name: str, q: Union[str, None] = None):
    return {"Name": name, "Message": "Hello, " + name}


@router.post("/post_method")
def post_with_body(request: RequestBody):
    return {"Name": request.name,
            "Description": request.description,
            "Square": (0 if request.some_number is None
                       else request.some_number ** 2)
            }
