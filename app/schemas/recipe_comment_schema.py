from pydantic import BaseModel

class CreateRecipeCommentSchema(BaseModel):
    comment: str
    