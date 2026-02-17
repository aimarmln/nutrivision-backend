from pydantic import BaseModel

class RecipeCommentSchema(BaseModel):
    id: str
    user: str
    text: str
    sentiment: str
