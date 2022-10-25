from typing import Union
from pydantic import BaseModel, UUID4


class RequestBody(BaseModel):
    name: str
    description: Union[str, None] = None
    some_number: Union[int, None] = None


class RabbitCountRequest(BaseModel):
    value: int


class RabbitCountUuid(BaseModel):
    task_id: UUID4
