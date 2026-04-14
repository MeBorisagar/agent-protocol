from fastapi import FastAPI
from protocol.schemas.message import BaseMessage, MessageType
import asyncio

app = FastAPI()


@app.post("/receive")
async def receive(msg: BaseMessage):

    if msg.type == MessageType.REQUEST:

        if msg.action == "task.execute":

            # simulate long task
           
            await asyncio.sleep(5)

            return {
                "type": "RESPONSE",
                "action": "task.execute",
                "payload": {
                    "result": "Processed async task"
                }
            }

    return {"status": "ignored"}