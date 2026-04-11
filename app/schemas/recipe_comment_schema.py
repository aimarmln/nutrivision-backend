from pydantic import BaseModel, PositiveInt
from datetime import datetime
from typing import Optional

class CommentsListQueryParams(BaseModel):
    last_created_at: Optional[datetime] = None
    limit: Optional[PositiveInt] = 10

class CreateRecipeCommentSchema(BaseModel):
    comment: str
    