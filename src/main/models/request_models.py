from typing import Union
from pydantic import BaseModel


class RequestBody(BaseModel):
    name: str
    description: Union[str, None] = None
    some_number: Union[int, None] = None
