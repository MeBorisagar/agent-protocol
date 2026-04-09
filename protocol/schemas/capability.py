from pydantic import BaseModel
from typing import Dict, Any


class Capability(BaseModel):
    name: str
    description: str

    input_schema: Dict[str, Any]
    output_schema: Dict[str, Any]