import unittest
import json
from uuid import uuid4
from consumer.consumer_count import CountConsumer


class TestCountSubscriber(unittest.TestCase):
    def __init__(self, methodName: str = ...) -> None:
        super().__init__(methodName)
        self.subscriber = CountConsumer()

    def test_count(self):
        self.assertEqual(3**3, self.subscriber.count_result(3))  # sleeps 5 sec
        self.assertEqual(5**3, self.subscriber.count_result(5))  # sleeps 5 sec

    def test_count_bad_data(self):
        self.assertEqual(0, self.subscriber.count_result("abc"))
        self.assertEqual(0, self.subscriber.count_result(None))

    def test_process_message_good_data(self):
        self.assertTrue(self.subscriber.process_message(None,
                                                        None,
                                                        None,
                                                        json.dumps({
                                                            "uuid":
                                                            str(uuid4()),
                                                            "a": 13
                                                        })))

    def test_process_message_bad_data(self):
        self.assertFalse(self.subscriber.process_message(None,
                                                         None,
                                                         None,
                                                         json.dumps({
                                                             "uuid":
                                                             str(uuid4()),
                                                             "a": "abc"
                                                            })))
        self.assertFalse(self.subscriber.process_message(None,
                                                         None,
                                                         None,
                                                         json.dumps({
                                                             "uuid":
                                                             str(uuid4()),
                                                         })))
        self.assertFalse(self.subscriber.process_message(None,
                                                         None,
                                                         None,
                                                         json.dumps({
                                                         })))
        self.assertFalse(self.subscriber.process_message(None,
                                                         None,
                                                         None,
                                                         json.dumps({
                                                             "a": 44
                                                         })))

    def test_redis(self):
        key = uuid4()
        self.subscriber.save_result(key, 5)
        self.assertEqual(int(self.subscriber.r.get(str(key))), 5)


if __name__ == "__main__":
    unittest.main()
