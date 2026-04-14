import httpx
import time

SERVER = "http://localhost:8000"


def send_task():
    msg = {
        "sender": "agent_a",
        "receiver": "agent_b",
        "type": "REQUEST",
        "action": "task.execute",
        "payload": {
            "task_id": "t1",
            "description": "heavy processing"
        }
    }

    res = httpx.post(f"{SERVER}/message", json=msg)
    data = res.json()

    task_id = data["task_id"]
    print("Task submitted:", task_id)

    # Poll
    while True:
        status = httpx.get(f"{SERVER}/tasks/{task_id}").json()
        print("Status:", status)

        if status["status"] in ["COMPLETED", "FAILED"]:
            break

        time.sleep(2)


if __name__ == "__main__":
    send_task()