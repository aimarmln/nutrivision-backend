# from langchain.tools import ToolRuntime, tool
# from langchain.agents import create_agent, AgentState
# from langchain.messages import SystemMessage, RemoveMessage
# from langgraph.graph.message import REMOVE_ALL_MESSAGES
# from langgraph.runtime import Runtime
# from langchain_groq import ChatGroq
# from typing import List, Optional, Literal, Any
# from pydantic import BaseModel, Field
# from datetime import date
# from dataclasses import dataclass
# from app.services.user_service import UserService
# from app.repositories.food_repository import FoodRepository
# from app.schemas.food_log_schema import BulkAddFoodLogItem, BulkUpdateFoodLogItem
# from app.schemas.user_schema import UpdateUserProfileSchema
# from app.services.food_log_service import FoodLogService
# from app.constants.food_log import MealType
# from app.constants.user import ActivityLevel, MainGoal
# from app.config import Config
# from langgraph.checkpoint.postgres import PostgresSaver  
# from langchain.agents.middleware import SummarizationMiddleware, before_model
# from app.config import Config


# # ================================
# # CONTEXT
# # ================================

# @dataclass
# class Context:
#     user_id: int

# # ================================
# # TOOLS
# # ================================

# class GetTodayFoodLogsInput(BaseModel):
#     meal_types: Optional[List[MealType]] = Field(
#         default=None,
#         description="Jenis catatan makanan: Breakfast, Lunch, Dinner, Snack. Jika kosong, ambil semua, contoh: ['Breakfast', 'Dinner'], Jika info dari user tidak menyebutkan meal_type, berarti None (ambil semua)"
#     )

# @tool(args_schema=GetTodayFoodLogsInput)
# def get_today_food_logs(meal_types: Optional[List[MealType]], runtime: ToolRuntime[Context]) -> dict:
#     """
#     Ambil daftar makanan yang dicatat hari ini
#     """

#     try:
#         user_id = runtime.context.user_id

#         logs = FoodLogService.get_today_logs(user_id, meal_types=meal_types)

#         if not logs:
#             return {
#                 "logs": [],
#                 "notes": f"Belum ada makanan dicatat di {', '.join([mt.value for mt in meal_types]) if meal_types else 'hari ini'}"
#             }

#         all_meals = meal_types or [mt for mt in MealType]

#         grouped = {
#             mt.value: {
#                 "items": [],
#                 "is_empty": True,
#                 "totals": {
#                     "calories": 0,
#                     "carbs": 0,
#                     "proteins": 0,
#                     "fats": 0
#                 }
#             }
#             for mt in all_meals
#         }

#         for log in logs:
#             serving = log.serving
#             factor = log.number_of_units / serving.number_of_units
#             calories = serving.calories_kcal * factor
#             carbs = serving.carbohydrate_g * factor
#             proteins = serving.protein_g * factor
#             fats = serving.fat_g * factor

#             mt = log.meal_type.value

#             group = grouped[mt]

#             group["items"].append({
#                 "log_id": log.id,
#                 "food_id": log.food_id,
#                 "food_name": log.food.name,
#                 "number_of_units": log.number_of_units,
#                 "serving_unit": log.serving.serving_unit,
#                 "calories": round(calories),
#                 "carbs": round(carbs, 1),
#                 "proteins": round(proteins, 1),
#                 "fats": round(fats, 1)
#             })

#             group["totals"]["calories"] += calories
#             group["totals"]["carbs"] += carbs
#             group["totals"]["proteins"] += proteins
#             group["totals"]["fats"] += fats

#             group["is_empty"] = False

#         user_summary = UserService.get_user_summary(user_id)["user_summary"]

#         return {
#             "logs": dict(grouped),
#             "summary": {
#                 "calories": f"{user_summary['calories_eaten']} / {user_summary['calories_per_day']} kcal",
#                 "carbs": f"{user_summary['carbohydrates_eaten']} / {user_summary['carbohydrates_per_day']} g",
#                 "proteins": f"{user_summary['proteins_eaten']} / {user_summary['proteins_per_day']} g",
#                 "fats": f"{user_summary['fats_eaten']} / {user_summary['fats_per_day']} g",
#             }
#         }
#     except Exception:
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }

# class AddFoodLogsInput(BaseModel):
#     logs: List[BulkAddFoodLogItem] = Field(
#         min_length=1,
#         description="List makanan yang akan ditambahkan"
#     )

# @tool(args_schema=AddFoodLogsInput)
# def add_food_logs(logs: List[BulkAddFoodLogItem], runtime: ToolRuntime[Context]) -> dict:
#     """
#     Tambah food log baru
#     """

#     try:
#         user_id = runtime.context.user_id

#         logged_foods = FoodLogService.bulk_add_food_logs(user_id, logs)
#         user_summary = UserService.get_user_summary(user_id)["user_summary"]

#         added_foods = [
#             {
#                 "log_id": log.id,
#                 "food_id": log.food_id,
#                 "food_name": log.food.name,
#                 "meal_type": log.meal_type.value,
#                 "number_of_units": log.number_of_units,
#                 "serving_unit": log.serving.serving_unit,
#                 "calories": round(log.serving.calories_kcal * (log.number_of_units / log.serving.number_of_units)),
#             }
#             for log in logged_foods
#         ]

#         return {
#             "status": "success",
#             "added_foods": added_foods,
#             "summary": {
#                 "calories": f"{user_summary['calories_eaten']} / {user_summary['calories_per_day']} kcal",
#                 "carbs": f"{user_summary['carbohydrates_eaten']} / {user_summary['carbohydrates_per_day']} g",
#                 "proteins": f"{user_summary['proteins_eaten']} / {user_summary['proteins_per_day']} g",
#                 "fats": f"{user_summary['fats_eaten']} / {user_summary['fats_per_day']} g",
#             }
#         }
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }

# class EditFoodLogsInput(BaseModel):
#     logs: List[BulkUpdateFoodLogItem] = Field(
#         min_length=1,
#         description="List log yang akan diedit"
#     )

# @tool(args_schema=EditFoodLogsInput)
# def edit_food_logs(logs: List[BulkUpdateFoodLogItem], runtime: ToolRuntime[Context]) -> dict:
#     """
#     Edit log makanan yang sudah dicatat
#     """
#     try:
#         user_id = runtime.context.user_id

#         updated_logs = FoodLogService.bulk_edit_food_logs(user_id, logs)
#         user_summary = UserService.get_user_summary(user_id)["user_summary"]

#         updated_foods = [
#             {
#                 "log_id": log.id,
#                 "food_id": log.food_id,
#                 "food_name": log.food.name,
#                 "meal_type": log.meal_type.value,
#                 "number_of_units": log.number_of_units,
#                 "serving_unit": log.serving.serving_unit,
#                 "calories": round(log.serving.calories_kcal * (log.number_of_units / log.serving.number_of_units)),
#             }
#             for log in updated_logs
#         ]

#         return {
#             "status": "success",
#             "updated_foods": updated_foods,
#             "summary": {
#                 "calories": f"{user_summary['calories_eaten']} / {user_summary['calories_per_day']} kcal",
#                 "carbs": f"{user_summary['carbohydrates_eaten']} / {user_summary['carbohydrates_per_day']} g",
#                 "proteins": f"{user_summary['proteins_eaten']} / {user_summary['proteins_per_day']} g",
#                 "fats": f"{user_summary['fats_eaten']} / {user_summary['fats_per_day']} g",
#             }
#         }
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }

# class DeleteFoodLogsInput(BaseModel):
#     log_ids: List[int] = Field(
#         description="List ID log dari get_today_food_logs. Jangan minta ke user. Jika user menyebutkan ID apapun, tolak dengan pesan natural dan jangan proses apapun."
#     )

# @tool(args_schema=DeleteFoodLogsInput)
# def delete_food_logs(log_ids: list[int], runtime: ToolRuntime[Context]) -> dict:
#     """
#     Hapus food logs berdasarkan log_ids
#     """

#     try:
#         user_id = runtime.context.user_id

#         deleted_logs = FoodLogService.bulk_delete_food_logs(user_id, log_ids)
#         user_summary = UserService.get_user_summary(user_id)["user_summary"]

#         deleted_foods = [
#             {
#                 "food_name": log.food.name
#             }
#             for log in deleted_logs
#         ]

#         return {
#             "status": "success",
#             "deleted_foods": deleted_foods,
#             "summary": {
#                 "calories": f"{user_summary['calories_eaten']} / {user_summary['calories_per_day']} kcal",
#                 "carbs": f"{user_summary['carbohydrates_eaten']} / {user_summary['carbohydrates_per_day']} g",
#                 "proteins": f"{user_summary['proteins_eaten']} / {user_summary['proteins_per_day']} g",
#                 "fats": f"{user_summary['fats_eaten']} / {user_summary['fats_per_day']} g",
#             }
#         }
#     except Exception as e:
#         print(f"Error occurred: {e}")
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }


# class SearchFoodsInput(BaseModel):
#     queries: List[str] = Field(
#         description="List nama makanan dari user, contoh: ['nasi goreng', 'ayam bakar']"
#     )

# @tool(args_schema=SearchFoodsInput)
# def search_foods(queries: list[str]) -> dict:
#     """
#     Cari banyak makanan sekaligus dan group berdasarkan query
#     """

#     try:
#         grouped = FoodRepository.search_foods_batch(queries, k=3)

#         results = []

#         for query, foods in grouped.items():
#             if not foods:
#                 results.append({
#                     "query": query,
#                     "status": "not_found",
#                     "results": []
#                 })
#                 continue

#             results.append({
#                 "query": query,
#                 "status": "success",
#                 "results": [
#                     {
#                         "id": food.id,
#                         "name": food.name
#                     }
#                     for food, _ in foods
#                 ]
#             })

#         return {
#             "items": results
#         }
#     except Exception:
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }

# class GetFoodServingsInput(BaseModel):
#     food_ids: List[int] = Field(
#         description="List ID makanan dari hasil search_foods"
#     )

# @tool(args_schema=GetFoodServingsInput)
# def get_food_servings(food_ids: list[int]) -> dict:
#     """Ambil daftar serving untuk suatu makanan"""

#     try:
#         foods = FoodRepository.find_servings_by_food_ids(food_ids)

#         food_map = {food.id: food for food in foods}

#         results = []

#         for food_id in food_ids:
#             food = food_map.get(food_id)

#             if not food:
#                 results.append({
#                     "food_id": food_id,
#                     "status": "not_found",
#                     "servings": []
#                 })
#                 continue

#             servings = sorted(food.servings, key=lambda s: not s.is_default)

#             results.append({
#                 "food_id": food_id,
#                 "food_name": food.name,
#                 "status": "success",
#                 "servings": [
#                     {
#                         "id": s.id,
#                         "number_of_units": s.number_of_units,
#                         "serving_unit": s.serving_unit,
#                         "calories": s.calories_kcal,
#                         "proteins": s.protein_g,
#                         "carbs": s.carbohydrate_g,
#                         "fats": s.fat_g,
#                         "is_default": s.is_default
#                     }
#                     for s in servings
#                 ]
#             })

#         return {
#             "items": results
#         }
#     except Exception:
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }

# @tool(args_schema=UpdateUserProfileSchema)
# def update_user_profile(
#     runtime: ToolRuntime[Context], 
#     name: Optional[str] = None,
#     birthday: Optional[date] = None,
#     height_cm: Optional[float] = None,
#     weight_kg: Optional[float] = None,
#     activity_level: Optional[ActivityLevel] = None,
#     main_goal: Optional[MainGoal] = None,
# ) -> dict:
#     """Update profil user, jika belum tahu datanya bisa ambil dari get_user_data tool"""

#     try:
#         user_id = runtime.context.user_id

#         data = UpdateUserProfileSchema(
#             name=name,
#             birthday=birthday,
#             height_cm=height_cm,
#             weight_kg=weight_kg,
#             activity_level=activity_level,
#             main_goal=main_goal
#         )

#         UserService.update_user_profile(user_id, data)

#         updated_fields = {
#             k: v for k, v in data.model_dump().items() if v is not None
#         }

#         affecting_fields = ['birthday', 'height_cm', 'weight_kg', 'activity_level', 'main_goal']
#         is_affecting = any(field in affecting_fields for field in updated_fields)

#         response = {
#             "status": "success",
#             "message": "Profil berhasil diperbarui",
#             "updated_fields": updated_fields
#         }

#         if is_affecting:
#             user_summary = UserService.get_user_summary(user_id)
#             summary = user_summary['user_summary']

#             response["summary"] = {
#                 "calories_per_day": summary['calories_per_day'],
#                 "carbohydrates_per_day": summary['carbohydrates_per_day'],
#                 "proteins_per_day": summary['proteins_per_day'],
#                 "fats_per_day": summary['fats_per_day']
#             }

#         return response
#     except Exception:
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }


# UserField = Literal[
#     "name", "birthday", "age", "height_cm", "weight_kg",
#     "activity_level", "main_goal", "bmi", "bmi_status"
# ]

# class GetUserDataInput(BaseModel):
#     fields: Optional[List[UserField]] = Field(
#         default=None,
#         description="Field profile yang ingin diambil. Contoh: ['weight_kg', 'height_cm']"
#     )

# @tool(args_schema=GetUserDataInput)
# def get_user_data(fields: Optional[List[UserField]], runtime: ToolRuntime[Context]) -> dict:
#     """
#     Ambil profile/data user.
#     """

#     try:
#         user_id = runtime.context.user_id
#         user_data = UserService.get_user_profile(user_id)
#         if fields:
#             return {k: user_data[k] for k in fields}
#         return user_data
#     except Exception:
#         return {
#             "status": "error",
#             "message": "Terjadi kesalahan, coba lagi"
#         }


# # ================================
# # TOOLS LIST
# # ================================

# tools = [
#     get_today_food_logs,
#     add_food_logs,
#     edit_food_logs,
#     delete_food_logs,
#     search_foods,
#     get_food_servings,
#     update_user_profile,
#     get_user_data,
# ]

# # ================================
# # MODEL
# # ================================

# model = ChatGroq(
#     model="openai/gpt-oss-20b",
#     groq_api_key=Config.GROQ_API_KEY,
#     temperature=0.3,
#     reasoning_effort="low",
#     max_tokens=500,
# )

# # SUMMARIZATION
# # - Triggerred if messages >= 10 (token trigger is ignored here, i dont know was this works right or not)
# # - Always run before main model call
# # - Creates summary + 10 most recent messages
# # - I dont use this anymore because it seems like the main model can be distracted by the summary
# # - I just think that i just use the keep N messages middleware

# # summarization = SummarizationMiddleware(
# #     model=ChatGroq(
# #         model="llama-3.1-8b-instant",
# #         max_tokens=500,
# #         temperature=0
# #     ),
# #     trigger=("tokens", 1500),
# #     keep=("messages", 10), 
# # )

# # @before_model
# # def trim_messages(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
# #     """Keep only the last 5 messages to fit context window."""
# #     messages = state["messages"]

# #     if len(messages) <= 5:
# #         return None  # No changes needed

# #     # first_msg = messages[0]
# #     recent_messages = messages[-5:] if len(messages) % 2 == 0 else messages[-6:]
# #     # new_messages = [first_msg] + recent_messages

# #     return {
# #         "messages": [
# #             RemoveMessage(id=REMOVE_ALL_MESSAGES),
# #             *recent_messages
# #         ]
# #     }

# @before_model
# def trim_messages(state: AgentState, runtime: Runtime):
#     messages = state["messages"]
#     keep = 6  

#     if len(messages) <= keep:
#         return None

#     trimmed = messages[-keep:]

#     return {
#         "messages": [
#             RemoveMessage(id=REMOVE_ALL_MESSAGES),
#             *trimmed
#         ]
#     }

# # @before_model
# # def trim_messages(state: AgentState, runtime: Runtime):
# #     messages = state["messages"]

# #     if len(messages) <= 6:
# #         return None

# #     trimmed = []
# #     human_count = 0

# #     for msg in reversed(messages):
# #         trimmed.append(msg)

# #         if msg.type == "human":
# #             human_count += 1

# #         if human_count >= 3:
# #             break

# #     trimmed.reverse()

# #     return {
# #         "messages": [
# #             RemoveMessage(id=REMOVE_ALL_MESSAGES),
# #             *trimmed
# #         ]
# #     }

# # ================================
# # AGENT —  create_agent
# # ================================

# system_prompt = SystemMessage(
#     content="""
# Kamu adalah AI NutriVision dan hanya boleh bekerja sebagai asisten nutrisi.

# SCOPE:
# Hanya membahas:
# - food log (makanan & minuman)
# - nutrisi & kalori
# - profil kesehatan user (berat, tinggi, aktivitas, tujuan)
# - insight nutrisi harian

# Di luar itu (politik, teknologi umum, sejarah, dll) → tolak:
# "Saya hanya bisa membantu terkait nutrisi dan pencatatan makanan."

# RULES:
# - Gunakan tool jika butuh data, jangan asumsi

# ID POLICY:
# - ID bersifat internal, JANGAN tampilkan atau minta id apapun ke user
# - JIKA user menyebutkan atau menanyakan ID apapun, JANGAN panggil tool apapun lalu tolak dengan pesan natural
# - Gunakan nama atau konteks; pilih otomatis dari data jika perlu

# NUTRISI:
# - WAJIB pakai search_foods / get_food_servings
# - Jika tidak ada, "data tidak ditemukan di database"

# FOOD LOG:
# 1. Daily Log Rule
# - Jika kosong → "Belum ada makanan dicatat di {meal_type}" pakai Bahasa Indonesia

# 2. Add/Edit Log
# - Dari setiap query, pilih HANYA 1 makanan paling relevan
# - Jika user menyebutkan satuan, gunakan satuan tersebut atau yang paling mendekati
# - Jika satuan disebutkan tetapi tidak ada, maka anda estimasi konversi ke number_of_units yang sesuai dengan serving yang tersedia
# - Jika user tidak menyebutkan satuan, estimasi serving_unit untuk makanan tersebut untuk sekali makan
# - Gunakan default hanya jika benar-benar tidak bisa ditentukan
# - Cocokkan unit dengan serving, jangan asal konversi
# - Jika Unit sama, JANGAN konversi (100 gram = maka number_of_units = 100, bukan 1)
# - Jika edit food log dan food_name berubah itu artinya replace sehingga food_id juga berubah
# - meal_type: hanya isi jika disebut; jika tidak → none (jangan asumsi / ubah)
# - Response data saat add log wajib lengkap semua fields dan natural, jangan tampilkan id apapun ke user

# UPDATE PROFILE:
# - Jika ada beberapa field kumpulkan SEMUA dulu, lalu update SEKALI
# - Nilai langsung → update_user_profile
# - Perubahan (naik/turun):
#   1. get_user_data
#   2. hitung nilai baru
#   3. update_user_profile

# VALIDASI:
# - weight: 40-250 kg
# - height: 140-230 cm
# - Tampilkan: nilai lama + perubahan = hasil
# - Jika di luar batas, tampilkan batas + minta konfirmasi (JANGAN call tool)

# OUTPUT:
# - Selalu konfirmasi update
# - Jika ada summary, tampilkan ringkas dan insight singkat
# - Jawaban natural

# Prioritas: akurat
# """
# )

# checkpointer_cm = PostgresSaver.from_conn_string(Config.CHECKPOINT_DB_URL)
# checkpointer = checkpointer_cm.__enter__()
# checkpointer.setup()

# agent = create_agent(
#     model=model,
#     tools=tools,
#     system_prompt=system_prompt,
#     context_schema=Context,
#     middleware=[trim_messages],
#     checkpointer=checkpointer
# )