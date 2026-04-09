import httpx
from protocol.schemas.message import BaseMessage


class MessageRouter:
    def __init__(self, registry: dict):
        self.registry = registry

    async def route(self, msg: BaseMessage):
        receiver_url = self.registry.get(msg.receiver)

        if not receiver_url:
            return {"error": "Unknown receiver"}

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{receiver_url}/receive",
                json=msg.model_dump()
            )

        return response.json()