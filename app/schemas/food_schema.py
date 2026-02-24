from pydantic import BaseModel, PositiveInt
from typing import Optional

class FoodsListQueryParams(BaseModel):
    q: Optional[str] = None
    page: PositiveInt = 1      
    limit: PositiveInt = 20  
