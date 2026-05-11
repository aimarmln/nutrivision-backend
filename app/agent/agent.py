from langchain.agents import create_agent

from .model import model
from .tools import tools
from .context import Context
from .middleware import keep_user_and_last_ai_message
from .prompt import system_prompt
from .checkpoint import checkpointer

agent = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    context_schema=Context,
    middleware=[keep_user_and_last_ai_message],
    checkpointer=checkpointer
)