from fastapi import FastAPI
from protocol.schemas.message import BaseMessage
from protocol.schemas.registry import AgentInfo
from protocol.core.router import MessageRouter
from protocol.store.task_store import TaskStore
from protocol.schemas.task import TaskStatus

import uuid

app = FastAPI()

AGENT_REGISTRY = {
    "agent_a": "http://localhost:8001",
    "agent_b": "http://localhost:8002",

}
router = MessageRouter(AGENT_REGISTRY)
task_store = TaskStore()


@app.post("/register")
def register(agent: AgentInfo):
    AGENT_REGISTRY[agent.name] = agent.url
    return {"status": "registered"}


@app.post("/message")
async def route_message(msg: BaseMessage):

    #  Create task
    task_id = str(uuid.uuid4())
    task_store.create_task(task_id)

    # attach task_id to metadata
    if not msg.metadata:
        msg.metadata = {}

    msg.metadata["task_id"] = task_id

    # mark accepted
    task_store.update_status(task_id, TaskStatus.ACCEPTED)

    # async fire-and-forget
    import asyncio
    asyncio.create_task(process_message(msg, task_id))

    return {
        "status": "accepted",
        "task_id": task_id
    }


async def process_message(msg: BaseMessage, task_id: str):
    try:
        task_store.update_status(task_id, TaskStatus.RUNNING)

        response = await router.route(msg)
        
        if response :

            task_store.complete_task(task_id, response)
        else:
           
            task_store.fail_task(task_id, "No response from router")
    except Exception as e:
        
        task_store.fail_task(task_id, str(e))


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    task = task_store.get_task(task_id)
    if not task:
        return {"error": "Task not found"}
    return task