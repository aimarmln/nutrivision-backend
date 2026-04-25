from enum import Enum

class ChatMessageRole(str, Enum):
    USER = "User"
    ASSISTANT = "Assistant"

    def __str__(self) -> str:
        return str(self.value)
