from time import sleep
from typing import Union
import uuid
import pika
import json
import redis


class CountConsumer:
    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        self.channel.queue_declare('count_queue', durable=True)
        self.r = redis.Redis(
            host='127.0.0.1',
            port=6379,
            encoding='utf-8',
            decode_responses=True
        )

    def count_result(self, val: int) -> int:
        if not isinstance(val, int):
            return 0
        sleep(5)
        return (val**3)

    def save_result(self,
                    uuid: uuid.UUID,
                    res: int,
                    err: bool = False,
                    err_info: Union[str, None] = None
                    ) -> None:
        key = str(uuid)
        if err:
            self.r.set(key, json.dumps({"err": True, "err_info": err_info}))
        else:
            self.r.set(key, res)

    def process_message(self, ch, method, properties, body) -> bool:
        """Process message from RabbitMQ.
        If decoding fails, returns False
        If decoding fails later than from start, saves err info to Redis
        If everything is OK, returns True
        This function returns for testing purpose

        Args:
            ch (_type_): _description_
            method (_type_): _description_
            properties (_type_): _description_
            body (bytearray): must be application/json
        Ret:
            bool
        """
        body_json = None
        try:
            body_json = json.loads(body)
        except json.JSONDecodeError:
            return False
        if "uuid" not in body_json:
            return False
        try:
            _ = uuid.UUID(body_json['uuid'], version=4)
        except ValueError:
            return False
        if "a" not in body_json:
            self.save_result(body_json["uuid"], None,
                             err=True, err_info="No value")
            return False
        val = None
        try:
            val = int(body_json["a"])
        except ValueError:
            self.save_result(body_json["uuid"], None,
                             err=True, err_info="ValueError")
            return False
        res = self.count_result(val)
        self.save_result(body_json["uuid"], res)
        return True

    def listen(self):
        self.channel.basic_consume(queue='count_queue',
                                   on_message_callback=self.process_message,
                                   auto_ack=True)
        self.channel.start_consuming()

    def stop(self):
        self.channel.stop_consuming()


def main():
    c = CountConsumer()
    c.listen()


if __name__ == "__main__":
    main()
