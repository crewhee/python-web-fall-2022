import grpc

from definitions.builds.service_pb2 import PolynomialTask
from definitions.builds.service_pb2_grpc import MyServiceStub

from fastapi import FastAPI
from typing import Union
from models.polynomial_models import PolynomialAnswerResponse, PolynomialErrorResponse, PolynomialTaskRequest

app = FastAPI()

PolyAnswerType = Union[PolynomialAnswerResponse, PolynomialErrorResponse]

@app.post("/count")
async def count_polynomial(p: PolynomialTaskRequest) -> PolyAnswerType:
    """Allows to count polynomial value in point using remote service via gRPC

    Args:
        p (PolynomialTaskRequest): JSON with x and coeffs

    Returns:
        PolyAnswerType: error code or answer
    """
    with grpc.insecure_channel("localhost:3000") as channel:
        client = MyServiceStub(channel)
        try:
            result = client.CountPolynomial(
                PolynomialTask(
                    x=p.x,
                    coefficients=p.coefficients
                )
            )
        except grpc.RpcError as e:
            return PolynomialErrorResponse(error="Got RpcException with code: " + str(e.code()))
        if result:
            return PolynomialAnswerResponse(result=result.y)
        else:
            return PolynomialErrorResponse(error="Unknown exception")
