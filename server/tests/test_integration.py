import unittest

from grpc import StatusCode
from grpc_testing import server_from_dictionary, strict_real_time
from definitions.builds import service_pb2, service_pb2_grpc
from server import Service

class TestCase(unittest.TestCase):

    def __init__(self, methodName) -> None:
        super().__init__(methodName)
        
        myServicer = Service()
        servicers = {
            service_pb2.DESCRIPTOR.services_by_name['MyService']: myServicer
        }
        self.test_server = server_from_dictionary(
            servicers, strict_real_time())

    def test_hello(self):
        request = service_pb2.Null()
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(service_pb2.DESCRIPTOR
                .services_by_name['MyService']
                .methods_by_name['GetHello']),
            invocation_metadata={},
            request=request, timeout=1)

        response, metadata, code, details = method.termination()
        self.assertEqual(code, StatusCode.OK)
        self.assertEqual("Hello, friend", response.greeting)

    def test_count(self):
        request = service_pb2.PolynomialTask(
            x=5,
            coefficients=[1, 1, 1]
        )
        method = self.test_server.invoke_unary_unary(
            method_descriptor=(service_pb2.DESCRIPTOR
                .services_by_name['MyService']
                .methods_by_name['CountPolynomial']),
            invocation_metadata={},
            request=request, timeout=1)

        response, metadata, code, details = method.termination()
        self.assertEqual(code, StatusCode.OK)
        self.assertEqual(31, response.y)


if __name__ == '__main__':
    unittest.main()