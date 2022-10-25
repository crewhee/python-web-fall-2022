import json
import redis
from time import sleep
import unittest
import uuid
from fastapi.testclient import TestClient
from src.main.main import app

from consumer.consumer_count import CountConsumer


class RabbitRedisIntegraion(unittest.TestCase):
    client = TestClient(app)

    def setUp(self) -> None:
        return super().setUp()

    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)

    def test_send_and_recieve_message(self):
        subscriber = CountConsumer()

        key = uuid.uuid4()
        r = redis.Redis(
            host='127.0.0.1',
            port=6379,
            encoding='utf-8',
            decode_responses=True
        )

        self.assertTrue(
            subscriber
                .process_message(None, None, None, json.dumps({
                    "uuid": str(key),
                    "a": 4
                }
                )
                )
        )
        try:
            res = r.get(str(key))
            self.assertIsNotNone(res)
            self.assertEqual(int(res), 4**3)
        except ValueError:
            self.fail("Not int as result")
        r.close()

    def test_send_via_fastapi(self):
        response = self.client.post('/rabbit_simple', json={"value": 32})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["task_sent"])
        key = response.json()["task_id"]
        response = self.client.post(
            '/rabbit_simple/result', json={"task_id": key})
        self.assertDictEqual(response.json(), {
            "task_id": str(key),
            "err_info": "Not processed yet."
        })
        sleep(10)
        response = self.client.post(
            '/rabbit_simple/result', json={"task_id": key})
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertTrue('answer' in body)
        self.assertEqual(32**3, int(body['answer']))

    # def tearDown(self) -> None:
    #     self.r.close()
    #     self.subscriber.r.close()
    #     if self.subscriber.connection.is_open():
    #         self.subscriber.connection.close()
    #     return super().tearDown()


if __name__ == "__main__":
    unittest.main()
