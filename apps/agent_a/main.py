import httpx
import uuid

SERVER_URL = "http://localhost:8000"


def register():
    httpx.post(f"{SERVER_URL}/register", json={
        "name": "agent_a",
        "url": "http://localhost:8001"
    })


def discover_capabilities():
    res = httpx.get("http://localhost:8002/capabilities")
    return res.json()


def send_task():
    msg = {
        "message_id": str(uuid.uuid4()),
        "sender": "agent_a",
        "receiver": "agent_b",
        "type": "REQUEST",
        "action": "task.execute",
        "payload": {
            "task_id": "task-123",
            "description": "analyze logs"
        }
    }

    res = httpx.post(f"{SERVER_URL}/message", json=msg)
    print(res.json())


if __name__ == "__main__":
    register()
    print("Capabilities:", discover_capabilities())
    send_task()