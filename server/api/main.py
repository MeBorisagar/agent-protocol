from fastapi import FastAPI
from protocol.schemas.message import BaseMessage
from protocol.schemas.registry import AgentInfo
from protocol.core.router import MessageRouter

app = FastAPI()

AGENT_REGISTRY = {}

router = MessageRouter(AGENT_REGISTRY)


@app.get("/")
def root():
    return {"message": "Agent Protocol v0.2 Running"}


# Register Agent
@app.post("/register")
def register(agent: AgentInfo):
    AGENT_REGISTRY[agent.name] = agent.url
    return {"status": "registered"}


# List Agents
@app.get("/agents")
def list_agents():
    return AGENT_REGISTRY


#  Route Message
@app.post("/message")
async def route_message(msg: BaseMessage):
    return await router.route(msg)