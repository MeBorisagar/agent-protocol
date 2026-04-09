from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from enum import Enum
import uuid
from datetime import datetime, timezone


class MessageType(str, Enum):
    REQUEST = "REQUEST"
    RESPONSE = "RESPONSE"
    EVENT = "EVENT"
    ERROR = "ERROR"


class BaseMessage(BaseModel):
    message_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    sender: str
    receiver: str

    type: MessageType

    action: str  

    payload: Dict[str, Any]

    metadata: Optional[Dict[str, Any]] = None