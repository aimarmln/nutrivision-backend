from datetime import datetime
from pydantic import BaseModel, PositiveInt
from typing import Optional

class ChatSchema(BaseModel):
    message: str

class SessionsListQueryParams(BaseModel):
    page: Optional[PositiveInt] = 1      
    limit: Optional[PositiveInt] = 20  

class ChatMessagesQueryParams(BaseModel):
    cursor_created_at: Optional[datetime] = None
    cursor_id: Optional[int] = None
    limit: Optional[PositiveInt] = 20

# class TestServingSchema(BaseModel):
#     food_id: int
#     serving: str
