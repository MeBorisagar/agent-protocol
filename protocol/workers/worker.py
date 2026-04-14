import asyncio
import httpx
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from protocol.queue.redis_queue import dequeue_task
from protocol.store.task_store import TaskStore
from protocol.schemas.task import TaskStatus
from protocol.schemas.message import BaseMessage
from protocol.registry.capability_registry import CapabilityRegistry

task_store = TaskStore()
capability_registry = CapabilityRegistry()


async def resolve_agent(action: str):
    return capability_registry.resolve(action)


async def process_message(msg: BaseMessage, task_id: str):
    try:
        task_store.update_status(task_id, TaskStatus.RUNNING)

        agent_url = await resolve_agent(msg.action)

        if not agent_url:
            raise Exception(f"No agent found for action {msg.action}")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{agent_url}/receive",
                json=msg.model_dump()
            )

        result = response.json()

        task_store.complete_task(task_id, result)

    except Exception as e:
        task_store.fail_task(task_id, str(e))


async def worker_loop():
    while True:
        task_data = dequeue_task()

        msg = BaseMessage(**task_data)
        task_id = msg.metadata["task_id"]

        await process_message(msg, task_id)


if __name__ == "__main__":
    asyncio.run(worker_loop())