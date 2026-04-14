import json
import redis

r = redis.Redis(host='localhost', port=6379, decode_responses=True)

QUEUE_NAME = "agent_tasks"


def enqueue_task(message: dict):
    r.lpush(QUEUE_NAME, json.dumps(message))


def dequeue_task():
    _, task = r.brpop(QUEUE_NAME)  # blocking pop
    return json.loads(task)