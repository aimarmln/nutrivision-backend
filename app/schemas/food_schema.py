from pydantic import BaseModel, PositiveInt
from typing import Optional

class FoodsListQueryParams(BaseModel):
    q: Optional[str] = None
    page: Optional[PositiveInt] = 1      
    limit: Optional[PositiveInt] = 20  
