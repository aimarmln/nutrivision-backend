from uuid import UUID
from typing import Optional
from pydantic import BaseModel

class ChatSchema(BaseModel):
    message: str
    session_id: Optional[UUID] = None

class TestServingSchema(BaseModel):
    food_id: str
    serving: str
