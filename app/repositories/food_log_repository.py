from sqlalchemy.orm import joinedload
from typing import List
from datetime import date, datetime, time
from zoneinfo import ZoneInfo
from app.constants.food_log import MealType
from app.database import SessionLocal
from app.models.food import Food
from app.models.food_log import FoodLog

class FoodLogRepository:

    @staticmethod
    def save(food_log: FoodLog) -> FoodLog:
        with SessionLocal() as session:
            session.add(food_log)
            session.commit()
            return food_log
        
    @staticmethod
    def find_by_id_and_user(
        food_log_id: int,
        user_id: int,
        preload_user: bool = False,
        preload_food: bool = False,
        preload_serving: bool = False,
        preload_food_servings: bool = False
    ) -> FoodLog | None:
        with SessionLocal() as session:
            query = session.query(FoodLog).filter(
                FoodLog.id == food_log_id,
                FoodLog.user_id == user_id,
                FoodLog.is_deleted == False
            )

            # Conditional eager load
            if preload_user:
                query = query.options(joinedload(FoodLog.user))
            if preload_food:
                if preload_food_servings:
                    # preload food + all its servings
                    query = query.options(joinedload(FoodLog.food).joinedload(Food.servings))
                else:
                    query = query.options(joinedload(FoodLog.food))
            if preload_serving:
                query = query.options(joinedload(FoodLog.serving))

            return query.first()

    @staticmethod
    def find_by_user_id_and_date(
        user_id: int,
        log_date: date,
        meal_type: MealType = None,
        preload_food: bool = False,
        preload_serving: bool = False,
        preload_food_servings: bool = False
    ) -> List[FoodLog]:
        tz = ZoneInfo("Asia/Jakarta")  # UTC+7
        start_datetime = datetime.combine(log_date, time.min, tzinfo=tz)
        end_datetime = datetime.combine(log_date, time.max, tzinfo=tz)

        with SessionLocal() as session:
            query = session.query(FoodLog).filter(
                FoodLog.user_id == user_id,
                FoodLog.created_at >= start_datetime,
                FoodLog.created_at <= end_datetime,
                FoodLog.is_deleted == False
            )

            # Conditional eager load
            if meal_type:
                query = query.filter(FoodLog.meal_type == meal_type)
            if preload_food:
                if preload_food_servings:
                    query = query.options(joinedload(FoodLog.food).joinedload(Food.servings))
                else:
                    query = query.options(joinedload(FoodLog.food))
            if preload_serving:
                query = query.options(joinedload(FoodLog.serving))

            return query.all()
        
    # AI utilities
    @staticmethod
    def bulk_save(logs: list[FoodLog]):
        with SessionLocal() as session:
            for log in logs:
                session.merge(log)  # attach ke session
            
            session.commit()

    @staticmethod
    def find_many_by_ids_and_user(
        log_ids: list[int],
        user_id: int,
        preload_food: bool = False,
        preload_serving: bool = False,
        preload_food_servings: bool = False
    ) -> List[FoodLog]:
        with SessionLocal() as session:
            query = session.query(FoodLog).filter(
                FoodLog.id.in_(log_ids),
                FoodLog.user_id == user_id,
                FoodLog.is_deleted == False
            )

            # Conditional eager load
            if preload_food:
                if preload_food_servings:
                    query = query.options(joinedload(FoodLog.food).joinedload(Food.servings))
                else:
                    query = query.options(joinedload(FoodLog.food))
            if preload_serving:
                query = query.options(joinedload(FoodLog.serving))
                
            return query.all()
        
    