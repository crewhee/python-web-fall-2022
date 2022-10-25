from fastapi import APIRouter
import pika
import json
from pydantic import BaseModel, UUID4
from uuid import uuid4
import redis

rabbit_router = APIRouter()


class RabbitCountRequest(BaseModel):
    value: int


class RabbitCountUuid(BaseModel):
    task_id: UUID4


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


@rabbit_router.post("/rabbit_simple/result")
def rabbit_response(req: RabbitCountUuid):
    r = redis.Redis(
        host='127.0.0.1',
        port=6379,
        encoding='utf-8',
        decode_responses=True
    )
    res = r.get(str(req.task_id))
    r.close()
    if res is None:
        return {
            "task_id": str(req.task_id),
            "err_info": "Not processed yet."
        }
    try:
        return {
            "task_id": str(req.task_id),
            "answer": int(res)
        }
    except ValueError:
        ans = json.loads(res)
        return {
            "task_id": str(req.task_id),
            "err_info": ans['err_info']
        }
