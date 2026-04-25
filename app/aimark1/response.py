from pydantic import BaseModel
from typing import Literal

class AiResponse(BaseModel):
    intent: Literal["log_food", "delete_food", "chat", "ask"]
    message: str