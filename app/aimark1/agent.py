from langchain.agents import create_agent
from app.aimark1.context import UserContext
from app.aimark1.middleware import trim_messages
from app.aimark1.tools import build_tools
from app.aimark1.prompts import system_prompt
from app.aimark1.memory import checkpointer
from app.aimark1.response import AiResponse
from app.extensions import llm

def build_agent():
    agent = create_agent(
        model=llm,
        tools=build_tools(),
        system_prompt=system_prompt,
        checkpointer=checkpointer,
        context_schema=UserContext,
        middleware=[trim_messages] 
    )

    return agent    

agent = build_agent()