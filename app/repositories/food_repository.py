import uuid
from sqlalchemy import case, func
from sqlalchemy.orm import joinedload
from app.constants.food import FOOD_CATEGORY_ORDER
from app.database import SessionLocal
from app.models.food import Food

class FoodRepository:

    @staticmethod
    def find_all_paginated(
        page: int = 1,
        limit: int = 20,
        search_query: str | None = None,
        preload_servings: bool = False
    ):
        with SessionLocal() as session:
            query = session.query(Food).filter(Food.is_deleted == False)

            # Full-text search
            if search_query:
                ts_query = func.plainto_tsquery('simple', search_query)
                query = query.filter(Food.search_vector.op('@@')(ts_query))

            # Preload servings
            if preload_servings:
                query = query.options(joinedload(Food.servings))
                
            # Custom category ordering (like pandas Categorical)
            category_case = case(
                {category: index for index, category in enumerate(FOOD_CATEGORY_ORDER)},
                value=Food.category,
                else_=len(FOOD_CATEGORY_ORDER)
            )

            query = query.order_by(
                category_case,      # Custom category order
                Food.subcategory.asc(),
                Food.name.asc()
            )

            offset_value = (page - 1) * limit

            return (
                query
                .offset(offset_value)
                .limit(limit)
                .all()
            )

    @staticmethod
    def find_by_id(id: uuid.UUID, preload_servings: bool = False) -> Food | None:
        with SessionLocal() as session:
            query = session.query(Food).filter(Food.id == id, Food.is_deleted == False)
            if preload_servings:
                query = query.options(joinedload(Food.servings))
            return query.first()
        
    @staticmethod
    def find_by_yolo_labels(yolo_labels: list[str], preload_servings: bool = False) -> list[Food]:
        with SessionLocal() as session:
            query = session.query(Food).filter(
                Food.yolo_label.in_(yolo_labels),
            )
            if preload_servings:
                query = query.options(joinedload(Food.servings))
            return query.all()          
        
    @staticmethod
    def count_all(search_query: str | None = None) -> int:
        with SessionLocal() as session:
            query = session.query(Food).filter(Food.is_deleted == False)
            if search_query:
                ts_query = func.plainto_tsquery('simple', search_query)
                query = query.filter(Food.search_vector.op('@@')(ts_query))
            return query.count()
    