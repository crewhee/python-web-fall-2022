from typing import List
from pydantic import BaseModel


class PolynomialTaskRequest(BaseModel):
    x: int
    coefficients: List[int]


class PolynomialErrorResponse(BaseModel):
    error: str

class PolynomialAnswerResponse(BaseModel):
    result: int