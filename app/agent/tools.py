from langchain.tools import tool
from app.services.food_log_service import FoodLogService
from app.services.user_service import UserService


@tool
def get_today_food_logs(user_id: str) -> list:
    """Ambil semua makanan hari ini"""
    logs = FoodLogService.get_today_logs(user_id)

    return [
        {
            "id": str(log.id),
            "name": log.food.name,
            "amount": log.number_of_units
        }
        for log in logs
    ]


@tool
def delete_food_log(user_id: str, log_id: str) -> str:
    """Hapus food log"""
    FoodLogService.delete_food_log(user_id, log_id)

    summary = UserService.get_user_summary(user_id)

    return "Food log berhasil dihapus, sisa kalori hari ini adalah " + str(summary["user_summary"]["calories_left"])