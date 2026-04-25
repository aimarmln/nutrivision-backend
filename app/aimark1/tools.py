from langchain.tools import tool, ToolRuntime
from app.aimark1.context import UserContext
from app.constants.food_log import MealType
from app.services.food_log_service import FoodLogService
from app.services.user_service import UserService
from app.repositories.food_repository import FoodRepository
from app.schemas.food_log_schema import CreateFoodLogSchema
from app.schemas.user_schema import UpdateUserProfileSchema
from langgraph.types import Command
from langchain.messages import ToolMessage


def build_tools():

    @tool
    def get_today_food_logs(
        runtime: ToolRuntime[UserContext],
        meal_type: MealType = None
    ) -> Command:
        """
        Mengambil daftar makanan yang dicatat hari ini
        """

        user_id = runtime.context.user_id
        logs = FoodLogService.get_today_logs(user_id, meal_type=meal_type)

        print("TOOL DEBUG - get_today_food_logs:")
        print("Running get_today_food_logs with user_id:", user_id)
        print("Running get_today_food_logs with meal_type:", meal_type if meal_type else "All")

        data = [
            {
                "id": str(log.id),
                "name": log.food.name,
                "calories": int(log.serving.calories_kcal),
                "amount": int(log.number_of_units)
            }
            for log in logs
        ]

        return Command(
            update={
                "last_food_logs": data,
                "messages": [
                    ToolMessage(
                        content="Berhasil mengambil data makanan",
                        tool_call_id=runtime.tool_call_id
                    )
                ]
            }
        )

        # if not data:
        #     return f"Belum ada makanan yang dicatat di {meal_type if meal_type else 'hari ini'}"

        # return """
        #     Berikut adalah daftar makanan yang dicatat hari ini:
        #     """ + "\n".join([f"- {d['name']} ({d['amount']} porsi, {d['calories']} kcal)" for d in data])
    
    @tool
    def delete_food_log(
        selection: str,
        runtime: ToolRuntime[UserContext]
    ) -> str:
        """Hapus catatan makanan berdasarkan nama atau nomor dari daftar terakhir"""

        user_id = runtime.context.user_id
        logs = runtime.state.get("last_food_logs", [])

        if not logs:
            return "Belum ada data makanan. Coba lihat daftar dulu ya."

        # pilih berdasarkan nomor
        if selection.isdigit():
            idx = int(selection) - 1
            if idx < 0 or idx >= len(logs):
                return "Pilihan tidak valid"
            target = logs[idx]

        else:
            target = next(
                (l for l in logs if selection.lower() in l["name"].lower()),
                None
            )

        if not target:
            return "Makanan tidak ditemukan"

        FoodLogService.delete_food_log(user_id, target["id"])

        return f"{target['name']} berhasil dihapus"

    # @tool
    # def prepare_food_selection(runtime: ToolRuntime[UserContext]) -> Command:
    #     """WAJIB digunakan saat user ingin hapus/edit tanpa menyebut item"""

    #     user_id = runtime.context.user_id
    #     logs = FoodLogService.get_today_logs(user_id)

    #     data = [
    #         {
    #             "id": str(log.id),
    #             "name": log.food.name,
    #             "calories": int(log.serving.calories_kcal),
    #             "amount": int(log.number_of_units)
    #         }
    #         for log in logs
    #     ]

    #     return Command(
    #         update={
    #             "last_food_logs": data
    #         }
    #     )

    # @tool
    # def delete_food_by_selection(
    #     selection: str,
    #     runtime: ToolRuntime[UserContext]
    # ) -> str:
    #     """Hapus makanan berdasarkan pilihan user (nama atau nomor)"""
        
    #     user_id = runtime.context.user_id
    #     logs = runtime.state.get("last_food_logs", [])

    #     if not logs:
    #         return "Data makanan belum tersedia"

    #     # support: "1"
    #     if selection.isdigit():
    #         idx = int(selection) - 1
    #         if idx < 0 or idx >= len(logs):
    #             return "Pilihan tidak valid"
    #         target = logs[idx]
    #     else:
    #         # support: "ayam bakar"
    #         target = next(
    #             (l for l in logs if selection.lower() in l["name"].lower()),
    #             None
    #         )

    #     if not target:
    #         return "Makanan tidak ditemukan"

    #     FoodLogService.delete_food_log(user_id, target["id"])

    #     return f"{target['name']} berhasil dihapus"

    # @tool
    # def create_food_log(
    #     food: str, 
    #     amount: int,
    #     runtime: ToolRuntime[UserContext]
    # ) -> str:
    #     """Log makanan user"""
    #     user_id = runtime.context.user_id

    #     foods = FoodRepository.get_foods_by_name(food)

    #     if not foods:
    #         return f"Makanan {food} tidak ditemukan"

    #     food_obj = foods[0]  

    #     default_serving = next(
    #         (s for s in food_obj.servings if s.is_default),
    #         None
    #     )

    #     req = CreateFoodLogSchema(
    #         food_id=food_obj.id,
    #         serving_id=default_serving.id,
    #         number_of_units=amount,
    #         meal_type="Lunch"
    #     )

    #     FoodLogService.create_food_log(user_id, req)

    #     return f"Berhasil mencatat {amount} porsi {food_obj.name}"


    # @tool
    # def delete_food_log(log_id: str, runtime: ToolRuntime[UserContext]) -> str:
    #     """Hapus food log, cari log makanan dengan nama query yang mirip, lalu hapus log makanan tersebut berdasarkan id"""
    #     user_id = runtime.context.user_id

    #     FoodLogService.delete_food_log(user_id, log_id)
    #     return f"Food log {log_id} berhasil dihapus"


    # @tool
    # def update_food_log(log_id: str, amount: int, runtime: ToolRuntime[UserContext]) -> str:
    #     """Update jumlah makanan"""
    #     user_id = runtime.context.user_id
    #     FoodLogService.update_food_log(user_id, log_id, amount)
    #     return f"Food log {log_id} berhasil diupdate jadi {amount}"


    # @tool
    # def get_daily_summary(runtime: ToolRuntime[UserContext]) -> str:
    #     """Ambil ringkasan nutrisi harian berisi summary kalori, protein, karbo, lemak dan makanan yang dicatat per hari"""
    #     user_id = runtime.context.user_id
    #     summary = UserService.get_user_summary(user_id)

    #     return f"""
    #         {summary}
    #     """
    
    # @tool 
    # def update_user_profile(data: UpdateUserProfileSchema, runtime: ToolRuntime[UserContext]) -> str:
    #     """Update profil user"""
    #     user_id = runtime.context.user_id
    #     UserService.update_user_profile(user_id, data)

    #     user_summary = UserService.get_user_summary(user_id)

    #     return "Profil berhasil diupdate, user jadi memiliki data sebagai berikut: " + str(user_summary)
    
    # @tool
    # def get_user_profile(runtime: ToolRuntime[UserContext]) -> str:
    #     """Profile user berisi nama, usia, jenis kelamin, bmi, bmr, activity level, dan lain lain"""
    #     user_id = runtime.context.user_id
    #     user = UserService.get_user_profile(user_id)

    #     return f"""
    #         {user}
    #     """

    # @tool
    # def search_food(food: str) -> str:
    #     """Cari makanan"""
    #     foods = FoodRepository.get_foods_by_name(food)

    #     if not foods:
    #         return "Tidak ditemukan"

    #     return """
    #         Ditemukan makanan berikut:
    #         """ + "\n".join([f"- {f}" for f in foods])                 

    return [
        # Food log tools
        get_today_food_logs,
        delete_food_log
        # prepare_food_selection,
        # delete_food_by_selection,
        # create_food_log,
        # delete_food_log,
        # update_food_log,
        # get_daily_summary,
        # search_food,
        # get_user_profile,
        # update_user_profile
    ]