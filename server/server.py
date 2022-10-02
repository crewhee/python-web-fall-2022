from concurrent.futures import ThreadPoolExecutor

import grpc
from services.polynomial_service import PolynomialService

from definitions.builds.service_pb2 import PolynomialResult, Hello
from definitions.builds.service_pb2_grpc import MyServiceServicer, add_MyServiceServicer_to_server


class Service(MyServiceServicer):
    def CountPolynomial(self, request, context):
        """_summary_

        Args:
            request (_type_): _description_
            context (_type_): _description_

        Returns:
            _type_: _description_
        """        
        s = PolynomialService()
        return PolynomialResult(y=s.count_polynomial(request.x, request.coefficients))
    
    def GetHello(self, request, context):
        return Hello(greeting="Hello, friend")


def execute_server():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    add_MyServiceServicer_to_server(Service(), server)
    server.add_insecure_port("[::]:3000")
    server.start()

    print("The server is up and running...")
    server.wait_for_termination()


if __name__ == "__main__":
    execute_server()
