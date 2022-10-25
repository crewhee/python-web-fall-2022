from fastapi import APIRouter
import pika
import json
from pydantic import BaseModel
from uuid import uuid4

rabbit_router = APIRouter()

class RabbitCountRequest(BaseModel):
    value: int

@rabbit_router.post("/rabbit_simple")
def rabbit_tasks(r: RabbitCountRequest):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='count_queue', durable=True)
    key = str(uuid4())
    channel.basic_publish(exchange='',
                          routing_key='count_queue',
                          body=json.dumps({"uuid": key, "a": r.value}))
    return {
        "task_sent": True,
        "task_id": key
    }
