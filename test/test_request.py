import unittest
import uuid
from fastapi.testclient import TestClient
from src.main.main import app

class RequestTest(unittest.TestCase):
    """Tests 

    Args:
        unittest (_type_): _description_
    """
    client = TestClient(app)

    def setUp(self) -> None:
        super().setUp()
    
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
    
    def test_bad_hard_request(self):
        response = self.client.post('/rabbit_simple', json={"val": "abc"})
        self.assertEqual(response.status_code, 422)
        response = self.client.post('/rabbit_simple', json={"32": 32})
        self.assertEqual(response.status_code, 422)
        response = self.client.post('/rabbit_simple', json={"val": None})
        self.assertEqual(response.status_code, 422)
        response = self.client.post('/rabbit_simple', json={"a": 42})
        self.assertEqual(response.status_code, 422)
    
    def test_good_request(self):
        response = self.client.post('/rabbit_simple', json={"value": 42})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["task_sent"])
        try:
            _ = uuid.UUID(response.json()["task_id"], version=4)
        except ValueError:
            self.fail("key is not valud uuid")
    

if __name__ == "__main__":
    unittest.main()