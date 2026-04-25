# ================================
# NutriVision Simple Agent (DELETE FOOD)
# 2-node loop: LLM <-> TOOLS
# ================================

from langchain.tools import tool
from langchain.messages import AnyMessage, SystemMessage, ToolMessage
from typing_extensions import TypedDict, Annotated
import operator

from langgraph.graph import StateGraph, START, END

# pakai LLM kamu
from app.extensions import llm

# services
from app.services.food_log_service import FoodLogService


# ================================
# TOOLS
# ================================

@tool
def get_today_food_logs(user_id: str) -> str:
    """
    Ambil daftar makanan hari ini.
    Return dalam bentuk list string agar mudah dibaca LLM.
    """

    logs = FoodLogService.get_today_logs(user_id)

    if not logs:
        return "Tidak ada makanan hari ini"

    result = []
    for i, log in enumerate(logs, 1):
        result.append(
            f"{i}. {log.food.name} (id: {log.id})"
        )

    return "\n".join(result)


@tool
def delete_food_log(user_id: str, log_id: str) -> str:
    """Hapus food log berdasarkan ID"""
    FoodLogService.delete_food_log(user_id, log_id)
    return f"Food dengan id {log_id} berhasil dihapus"


# daftar tools
tools = [get_today_food_logs, delete_food_log]
tools_by_name = {tool.name: tool for tool in tools}

# bind tools ke LLM
model_with_tools = llm.bind_tools(tools)


# ================================
# STATE
# ================================

class MessagesState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add]
    user_id: str
    llm_calls: int


# ================================
# LLM NODE
# ================================

def llm_call(state: MessagesState):
    """
    LLM menentukan:
    - apakah perlu call tool
    - atau jawab user
    """

    system_prompt = SystemMessage(
        content="""
Kamu adalah AI NutriVision untuk mencatat makanan.

RULES:
- Jika user ingin menghapus makanan:
    1. Panggil get_today_food_logs dulu
    2. Tampilkan ke user
    3. Minta user pilih nomor ATAU gunakan id
    4. Setelah jelas, panggil delete_food_log

- JANGAN menebak ID
- SELALU gunakan tool jika perlu data
- Jangan langsung hapus tanpa melihat daftar

Output harus natural ke user.
"""
    )

    response = model_with_tools.invoke(
        [system_prompt] + state["messages"]
    )

    return {
        "messages": [response],
        "llm_calls": state.get("llm_calls", 0) + 1
    }


# ================================
# TOOL NODE
# ================================

def tool_node(state: MessagesState):
    """
    Eksekusi tool yang diminta LLM
    """

    last_message = state["messages"][-1]

    results = []

    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]

        # inject user_id otomatis
        args = tool_call["args"]
        args["user_id"] = state["user_id"]

        observation = tool.invoke(args)

        results.append(
            ToolMessage(
                content=str(observation),
                tool_call_id=tool_call["id"]
            )
        )

    return {
        "messages": results
    }


# ================================
# ROUTER
# ================================

from typing import Literal

def should_continue(state: MessagesState) -> Literal["tool_node", END]:
    last = state["messages"][-1]

    if last.tool_calls:
        return "tool_node"

    return END


# ================================
# BUILD AGENT
# ================================

def build_agent():

    graph = StateGraph(MessagesState)

    graph.add_node("llm_call", llm_call)
    graph.add_node("tool_node", tool_node)

    graph.add_edge(START, "llm_call")

    graph.add_conditional_edges(
        "llm_call",
        should_continue,
        ["tool_node", END]
    )

    graph.add_edge("tool_node", "llm_call")

    return graph.compile()

agent = build_agent()