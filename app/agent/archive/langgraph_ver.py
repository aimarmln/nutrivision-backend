# from langchain.tools import ToolRuntime, tool
# from langgraph.runtime import Runtime
# from langchain.messages import AnyMessage, SystemMessage, ToolMessage
# from typing_extensions import TypedDict, Annotated
# from typing import List, Optional, Literal
# import operator
# from langchain_groq import ChatGroq
# from langgraph.prebuilt import ToolNode

# from langgraph.graph import StateGraph, START, END

# from dataclasses import dataclass

# from app.services.user_service import UserService
# from app.repositories.food_repository import FoodRepository
# from app.schemas.food_log_schema import BulkAddFoodLogSchema
# from app.schemas.user_schema import UpdateUserProfileSchema

# # services
# from app.services.food_log_service import FoodLogService
# from app.services.user_service import UserService
# from app.constants.food_log import MealType
# from app.config import Config

# # ================================
# # STATE
# # ================================

# class MessagesState(TypedDict):
#     messages: Annotated[list[AnyMessage], operator.add]
#     llm_calls: int

# @dataclass
# class Context:
#     user_id: str


# # ================================
# # TOOLS
# # ================================

# # Food log tools

# @tool
# def get_today_food_logs(meal_type: Optional[MealType], runtime: ToolRuntime[Context]) -> str:
#     """
#     Ambil daftar makanan yang dicatat hari ini

#     Args:
#         meal_type (MealType): Jenis makanan (Breakfast, Lunch, Dinner, Snack), optional
#     """

#     user_id = runtime.context.user_id

#     logs = FoodLogService.get_today_logs(user_id, meal_type=meal_type)

#     if not logs:
#         return f"Tidak ada makanan dicatat di {meal_type if meal_type else 'hari ini'}"
    
#     result = []
#     for log in logs:
#         serving = log.serving
#         factor = log.number_of_units / serving.number_of_units
#         calories = serving.calories_kcal * factor

#         result.append(
#             f"{log.food.name} {log.number_of_units} {log.serving.serving_unit} kalori: {round(calories)} id: {log.id}"
#         )

#     return "\n".join(result) + "\n Jangan show id ke user"


# @tool
# def delete_food_log(log_ids: list[int], runtime: ToolRuntime[Context]) -> str:
#     """
#     Hapus food log berdasarkan log_id

#     Args:
#         log_ids (List[int]): Daftar ID log makanan, jangan minta ke user, dapatkan dari output get_today_food_logs
#     """
#     user_id = runtime.context.user_id
    
#     deleted_logs = FoodLogService.bulk_delete_food_logs(user_id, log_ids)
#     user_summary = UserService.get_user_summary(user_id)

#     deleted_names = [log.food.name for log in deleted_logs]

#     return f"""
#     Berhasil menghapus: {", ".join(deleted_names)}
#     Anda sudah makan {user_summary['user_summary']['calories_eaten']} Kcal hari ini
#     Sisa kalori hari ini: {user_summary['user_summary']['calories_left']}
#     """.strip()

# @tool
# def add_food_log(
#     logs: BulkAddFoodLogSchema,
#     runtime: ToolRuntime[Context]
# ) -> str:
#     """
#     Tambah food log baru

#     Args:
#         logs (BulkAddFoodLogSchema): Daftar log makanan yang akan ditambahkan, dapatkan dari output search_food dan get_food_servings
#     """
#     user_id = runtime.context.user_id

#     logged_foods = FoodLogService.bulk_add_food_logs(user_id, logs)
#     user_summary = UserService.get_user_summary(user_id)

#     logged_food_names = [log.food.name for log in logged_foods]

#     return f"""
#     Berhasil menambahkan {", ".join(logged_food_names)}
#     Anda sudah makan {user_summary['user_summary']['calories_eaten']} Kcal hari ini
#     Sisa kalori hari ini: {user_summary['user_summary']['calories_left']}
#     """.strip()


# # Food & serving tools

# @tool
# def search_food(query: str) -> str:
#     """
#     Cari makanan berdasarkan nama (misal: nasi, ayam goreng)
#     """

#     foods = FoodRepository.get_foods_by_name(query, k=3)

#     if not foods[0]:
#         return "Makanan tidak ditemukan"

#     return "\n".join([
#         f"{food.name} (id: {food.id})"
#         for food, _ in foods
#     ])

# @tool
# def get_food_servings(food_id: int) -> str:
#     """
#     Ambil daftar serving untuk suatu makanan
#     """

#     food = FoodRepository.find_by_id(food_id, preload_servings=True)

#     if not food:
#         return "Food tidak ditemukan"

#     servings = sorted(food.servings, key=lambda s: not s.is_default)

#     return "\n".join([
#         f"{s.number_of_units} {s.serving_unit} ({s.description})"
#         f"(kalori: {s.calories_kcal}, protein: {s.protein_g}g, karbohidrat: {s.carbohydrate_g}g, lemak: {s.fat_g}g) id: {s.id} {'[default]' if s.is_default else ''}"
#         for s in servings
#     ])

# # Profile tools

# @tool 
# def update_user_profile(
#         data: UpdateUserProfileSchema, 
#         runtime: ToolRuntime[Context]
#     ) -> str:
#     """Update profil user, jika belum tahu datanya bisa ambil dari get_user_profile tool"""

#     user_id = runtime.context.user_id

#     UserService.update_user_profile(user_id, data)

#     user_summary = UserService.get_user_summary(user_id)

#     return f"""
#         Profil berhasil diperbarui. Kebutuhan kalori harianmu sekarang:
#         Kalori: {user_summary['user_summary']['calories_per_day']} Kcal
#         Karbohidrat: {user_summary['user_summary']['carbohydrates_per_day']} g
#         Protein: {user_summary['user_summary']['proteins_per_day']} g
#         Lemak: {user_summary['user_summary']['fats_per_day']} g
#     """.strip()

# UserField = Literal[
#     "name",
#     "birthday",
#     "age",
#     "height_cm",
#     "weight_kg",
#     "activity_level",
#     "main_goal",
#     "bmi",
#     "bmi_status"
# ]

# @tool
# def get_user_data(
#     fields: Optional[List[UserField]],
#     runtime: ToolRuntime[Context]
# ) -> dict:
#     """
#     Ambil profile user.

#     Args:
#         fields: Field yang ingin diambil.
#     """
#     user_id = runtime.context.user_id

#     print(f"Fetching user profile for user_id={user_id} with fields={fields}")

#     user_data = UserService.get_user_profile(user_id)

#     if fields:
#         return {k: user_data[k] for k in fields}

#     return user_data


# # daftar tools
# tools = [
#     get_today_food_logs, 
#     delete_food_log, 
#     add_food_log, 
#     search_food, 
#     get_food_servings, 
#     update_user_profile, 
#     get_user_data,
# ]

# tools_by_name = {tool.name: tool for tool in tools}

# print("Tools loaded:", list(tools_by_name.keys()))

# model = ChatGroq(
#     model="openai/gpt-oss-20b",
#     groq_api_key=Config.GROQ_API_KEY,
#     temperature=0.3,
#     reasoning_effort="low",
#     max_tokens=500
# )

# # bind tools ke LLM
# model_with_tools = model.bind_tools(tools)

# # ================================
# # LLM NODE
# # ================================

# def llm_call(state: MessagesState):
#     """
#     LLM menentukan:
#     - apakah perlu call tool
#     - atau jawab user
#     """

#     # system_prompt = SystemMessage(
#     #     content="""
#     #     Kamu adalah AI NutriVision aplikasi pencatatan kalori.

#     #     RULES:
#     #     - SELALU gunakan tool jika perlu data
#     #     - JANGAN menjawab berdasarkan asumsi
#     #     - REASONING singkat saja

#     #     Output harus natural ke user.
#     #     """
#     # )

#     system_prompt = SystemMessage(
#         content="""
#         Kamu adalah AI NutriVision untuk mencatat makanan.

#         RULES:
#         - Gunakan tool jika butuh data
#         - Jangan asumsi tanpa dasar
#         - Jawaban harus natural

#         FOOD LOGIC:

#         1. Pahami jumlah & unit user

#         2. Cocokkan unit dengan serving:
#         - Jika maknanya sama (contoh: potong ≈ porsi), langsung pakai
#         - Jangan konversi jika sudah cocok

#         3. Jika tidak cocok:
#         - Pilih serving terdekat
#         - Jika tetap tidak cocok → pakai default + konversi ke gram

#         4. Jangan pakai jumlah user jika unit beda tanpa konversi

#         Prioritas: akurat
#         """
#     )

#     response = model_with_tools.invoke(
#         [system_prompt] + state["messages"]
#     )

#     return {
#         "messages": [response],
#         "llm_calls": state.get("llm_calls", 0) + 1
#     }


# # ================================
# # TOOL NODE
# # ================================

# tool_node = ToolNode(tools)

# # def tool_node(state: MessagesState, runtime: Runtime[Context]):
# #     """
# #     Eksekusi tool yang diminta LLM
# #     """

# #     last_message = state["messages"][-1]

# #     results = []

# #     for tool_call in last_message.tool_calls:
# #         tool = tools_by_name[tool_call["name"]]

# #         observation = tool.invoke(
# #             tool_call["args"],
# #             runtime=runtime
# #         )

# #         results.append(
# #             ToolMessage(
# #                 content=str(observation),
# #                 tool_call_id=tool_call["id"]
# #             )
# #         )

# #     return {
# #         "messages": results
# #     }


# # ================================
# # ROUTER
# # ================================

# from typing import Literal

# def should_continue(state: MessagesState) -> Literal["tool_node", END]:
#     last = state["messages"][-1]

#     if last.tool_calls:
#         return "tool_node"

#     return END


# # ================================
# # BUILD AGENT
# # ================================

# def build_agent():

#     graph = StateGraph(
#         MessagesState,
#         context_schema=Context
#     )

#     graph.add_node("llm_call", llm_call)
#     graph.add_node("tool_node", tool_node)

#     graph.add_edge(START, "llm_call")

#     graph.add_conditional_edges(
#         "llm_call",
#         should_continue,
#         ["tool_node", END]
#     )

#     graph.add_edge("tool_node", "llm_call")

#     return graph.compile()

# agent = build_agent()

