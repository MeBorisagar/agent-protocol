import httpx
import uuid

def send_task():
    data = {
        "message_id": str(uuid.uuid4()),
        "sender": "agent_a",
        "receiver": "agent_b",
        "type": "TASK_REQUEST",
        "payload": {
            "task_id": "123",
            "description": "analyze logs"
        }
    }

    res = httpx.post("http://localhost:8001/message", json=data)
    print(res.json())

if __name__ == "__main__":
    send_task()