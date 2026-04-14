from fastapi import FastAPI
from protocol.schemas.message import BaseMessage
from protocol.schemas.registry import AgentInfo
from protocol.store.task_store import TaskStore
from protocol.schemas.task import TaskStatus
from protocol.queue.redis_queue import enqueue_task
from protocol.registry.capability_registry import CapabilityRegistry

import uuid
import httpx

app = FastAPI()

AGENT_REGISTRY = {
    "agent_a": "http://localhost:8001",
    "agent_b": "http://localhost:8002",

}
task_store = TaskStore()
capability_registry = CapabilityRegistry()


@app.post("/register")
async def register(agent: AgentInfo):
    """
    Agent registers itself + capabilities
    """

    AGENT_REGISTRY[agent.name] = agent.url

    # Fetch capabilities from agent
    async with httpx.AsyncClient() as client:
        res = await client.get(f"{agent.url}/capabilities")
        capabilities = res.json()

    # Register capabilities
    capability_registry.register(agent.name, agent.url, capabilities)

    return {"status": "registered", "capabilities": capabilities}


@app.get("/capabilities")
def list_capabilities():
    return capability_registry.capability_map


@app.post("/message")
async def route_message(msg: BaseMessage):

    task_id = str(uuid.uuid4())
    task_store.create_task(task_id)

    if not msg.metadata:
        msg.metadata = {}

    msg.metadata["task_id"] = task_id

    task_store.update_status(task_id, TaskStatus.ACCEPTED)

    # push to queue
    enqueue_task(msg.model_dump())

    return {
        "status": "accepted",
        "task_id": task_id
    }


@app.get("/tasks/{task_id}")
def get_task(task_id: str):
    return task_store.get_task(task_id)