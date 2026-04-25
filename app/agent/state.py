from typing import TypedDict, Annotated, List, Optional
from langchain.messages import AnyMessage
import operator


class AgentState(TypedDict):
    messages: Annotated[List[AnyMessage], operator.add]

    intent: Optional[str]
    food_query: Optional[str]

    last_food_logs: list
    selected_item: Optional[dict]

    user_id: str