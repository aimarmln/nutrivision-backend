import uuid
from sqlalchemy.orm import joinedload
from typing import List
from datetime import date, datetime, time, timezone
from app.database import SessionLocal
from app.models.food_log import FoodLog

class FoodLogRepository:

    @staticmethod
    def save(food_log: FoodLog) -> FoodLog:
        with SessionLocal() as session:
            session.add(food_log)
            session.commit()
            session.refresh(food_log)
            return food_log
        
    @staticmethod
    def find_by_id_and_user(
        food_log_id: uuid.UUID,
        user_id: uuid.UUID,
        preload_user: bool = False,
        preload_food: bool = False
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
                query = query.options(joinedload(FoodLog.food))

            return query.first()

    @staticmethod
    def find_by_user_id_and_date(user_id: uuid.UUID, log_date: date) -> List[FoodLog]:
        start_datetime = datetime.combine(log_date, time.min, tzinfo=timezone.utc)
        end_datetime = datetime.combine(log_date, time.max, tzinfo=timezone.utc)    

        with SessionLocal() as session:
            result = (
                session.query(FoodLog)
                .options(joinedload(FoodLog.food))
                .filter(
                    FoodLog.user_id == user_id,
                    FoodLog.created_at >= start_datetime,
                    FoodLog.created_at <= end_datetime,
                    FoodLog.is_deleted == False
                )
                .all()
            )
            
        return result
        