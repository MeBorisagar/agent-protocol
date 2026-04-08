from pydantic import BaseModel
from typing import Dict, Any

class BaseMessage(BaseModel):
    message_id: str
    sender: str
    receiver: str
    type: str
    payload: Dict[str, Any]