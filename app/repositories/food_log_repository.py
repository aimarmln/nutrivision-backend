from sqlalchemy.orm import joinedload
from typing import List, Optional
from datetime import date, datetime, time
from zoneinfo import ZoneInfo
from app.database import db_session
from app.models import Food, FoodLog, Serving
from app.constants.food_log import MealType

class FoodLogRepository:

    @staticmethod
    def save(food_log: FoodLog):
        db_session.add(food_log)
        db_session.flush()

    @staticmethod
    def find_by_id_and_user(
        food_log_id: int,
        user_id: int,
        preload_user: bool = False,
        preload_food: bool = False,
        preload_serving: bool = False,
        preload_food_servings: bool = False
    ) -> FoodLog | None:
        query = db_session.query(FoodLog).filter(
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
        meal_types: Optional[List[MealType]] = None,
        preload_food: bool = False,
        preload_serving: bool = False,
        preload_food_servings: bool = False
    ) -> List[FoodLog]:
        tz = ZoneInfo("Asia/Jakarta")  # UTC+7
        start_datetime = datetime.combine(log_date, time.min, tzinfo=tz)
        end_datetime = datetime.combine(log_date, time.max, tzinfo=tz)

        query = db_session.query(FoodLog).filter(
            FoodLog.user_id == user_id,
            FoodLog.created_at >= start_datetime,
            FoodLog.created_at <= end_datetime,
            FoodLog.is_deleted == False
        )

        # Conditional eager load
        if meal_types:
            query = query.filter(FoodLog.meal_type.in_(meal_types))
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
    def bulk_insert(logs: list[FoodLog]):
        db_session.add_all(logs)
        db_session.flush()

    @staticmethod
    def bulk_update(logs: list[FoodLog]):
        for log in logs:
            db_session.merge(log)

    @staticmethod
    def find_many_by_ids_and_user(
        log_ids: list[int],
        user_id: int,
        preload_food: bool = False,
        preload_serving: bool = False,
        preload_food_servings: bool = False
    ) -> List[FoodLog]:
        query = db_session.query(FoodLog).filter(
            FoodLog.id.in_(log_ids),
            FoodLog.user_id == user_id,
            FoodLog.is_deleted == False
        )

        # Conditional eager load
        if preload_food:
            if preload_food_servings:
                query = query.options(
                    joinedload(FoodLog.food).load_only(
                        Food.id, 
                        Food.name
                    ).joinedload(Food.servings).load_only(
                        Serving.id, 
                        Serving.calories_kcal, 
                        Serving.number_of_units, 
                        Serving.serving_unit
                    )
                )
            else:
                query = query.options(
                    joinedload(FoodLog.food).load_only(Food.id, Food.name)
                )
        if preload_serving:
            query = query.options(
                joinedload(FoodLog.serving).load_only(
                    Serving.id, 
                    Serving.calories_kcal, 
                    Serving.number_of_units, 
                    Serving.serving_unit
                )
            )
            
        return query.all()
        
    