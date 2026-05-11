from langchain.agents.middleware import after_agent
from langchain.agents import AgentState
from langgraph.runtime import Runtime
from langchain.messages import RemoveMessage, HumanMessage, AIMessage
from langgraph.graph.message import REMOVE_ALL_MESSAGES, AnyMessage
from typing import Any

KEEP_TURNS = 8

@after_agent
def keep_user_and_last_ai_message(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    messages = state["messages"]
    
    # Kelompokkan pesan per turn berdasarkan HumanMessage
    turns = []
    current_turn = []
    
    for msg in messages:
        if isinstance(msg, HumanMessage) and current_turn:
            turns.append(current_turn)
            current_turn = [msg]
        else:
            current_turn.append(msg)
    
    if current_turn:
        turns.append(current_turn)
    
    # Ambil N turn terakhir
    kept_turns = turns[-KEEP_TURNS:]
    
    # Dari tiap turn, ambil HumanMessage + AIMessage terakhir saja
    trimmed: list[AnyMessage] = []
    for turn in kept_turns:
        human_msgs = [m for m in turn if isinstance(m, HumanMessage)]
        ai_msgs = [m for m in turn if isinstance(m, AIMessage)]
        
        trimmed.extend(human_msgs)          # user message
        if ai_msgs:
            trimmed.append(ai_msgs[-1])     # hanya AI message terakhir di turn ini

    # Kalau hasil trim sama dengan messages sekarang, skip (tidak ada perubahan)
    trimmed_ids = [m.id for m in trimmed]
    current_ids = [m.id for m in messages]
    if trimmed_ids == current_ids:
        return None
    
    return {
        "messages": [
            RemoveMessage(id=REMOVE_ALL_MESSAGES),
            *trimmed
        ]
    }
