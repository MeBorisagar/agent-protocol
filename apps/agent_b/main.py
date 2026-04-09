from fastapi import FastAPI
from protocol.schemas.message import BaseMessage, MessageType

app = FastAPI()


@app.get("/capabilities")
def capabilities():
    return [
        {
            "name": "task.execute",
            "description": "Execute a generic task",
            "input_schema": {
                "type": "object",
                "properties": {
                    "task_id": {"type": "string"},
                    "description": {"type": "string"}
                }
            },
            "output_schema": {
                "type": "object",
                "properties": {
                    "result": {"type": "string"}
                }
            }
        }
    ]


@app.post("/receive")
async def receive(msg: BaseMessage):
    print("Agent B received:", msg)

    if msg.type == MessageType.REQUEST:
        if msg.action == "task.execute":
            return {
                "type": "RESPONSE",
                "action": "task.execute",
                "payload": {
                    "result": "Task completed successfully"
                }
            }

    return {"status": "ignored"}