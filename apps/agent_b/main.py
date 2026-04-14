from fastapi import FastAPI
from protocol.schemas.message import BaseMessage, MessageType
import asyncio

app = FastAPI()


@app.get("/capabilities")
def capabilities():
    return [
        {
            "name": "task.execute",
            "description": "Execute a task",
            "input_schema": {},
            "output_schema": {}
        }
    ]


@app.post("/receive")
async def receive(msg: BaseMessage):

    if msg.type == MessageType.REQUEST:

        if msg.action == "task.execute":

            await asyncio.sleep(5)

            return {
                "type": "RESPONSE",
                "action": "task.execute",
                "payload": {
                    "result": f"Executed by Agent B"
                }
            }

    return {"status": "ignored"}