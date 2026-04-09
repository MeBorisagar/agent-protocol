from pydantic import BaseModel


class AgentInfo(BaseModel):
    name: str
    url: str