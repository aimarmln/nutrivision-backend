from pydantic import BaseModel, PositiveInt
from typing import Optional

class RecipesListQueryParams(BaseModel):
    q: Optional[str] = None
    page: Optional[PositiveInt] = 1      
    limit: Optional[PositiveInt] = 20  

class RecipeCommentSchema(BaseModel):
    id: str
    user: str
    text: str
    sentiment: str
