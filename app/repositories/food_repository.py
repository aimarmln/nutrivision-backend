from sqlalchemy import case, func, or_, desc
from sqlalchemy.orm import joinedload
from app.constants.food import FOOD_CATEGORY_ORDER
from app.database import SessionLocal
from app.models.food import Food
from app.extensions import embeddings

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

            # Custom category ordering
            category_case = case(
                {category: index for index, category in enumerate(FOOD_CATEGORY_ORDER)},
                value=Food.category,
                else_=len(FOOD_CATEGORY_ORDER)
            )

            # Full-text search
            if search_query:
                ts_query = func.websearch_to_tsquery('simple', search_query)

                starts_with = case(
                    (Food.name.ilike(f"{search_query}%"), 1),
                    else_=0
                )

                exact_phrase = case(
                    (Food.name.ilike(f"%{search_query}%"), 1),
                    else_=0
                )

                base_rank = func.ts_rank(
                    Food.search_vector,
                    ts_query,
                    32
                )

                rank = (
                    base_rank +
                    starts_with * 3 +
                    exact_phrase * 2
                )

                query = (
                    query
                    .filter(
                        Food.search_vector.op('@@')(ts_query),
                        Food.is_deleted == False,
                    )
                    .order_by(
                        desc(rank),
                        category_case,
                        Food.subcategory.asc(),
                        Food.name.asc()
                    )
                )
            else:
                query = query.order_by(
                    category_case,
                    Food.subcategory.asc(),
                    Food.name.asc()
                )

            # Preload servings
            if preload_servings:
                query = query.options(joinedload(Food.servings))

            offset_value = (page - 1) * limit

            return (
                query
                .offset(offset_value)
                .limit(limit)
                .all()
            )

    @staticmethod
    def find_by_id(id: int, preload_servings: bool = False) -> Food | None:
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
    
    # AI utilities
    @staticmethod
    def get_foods_by_name(name: str, k: int = 3) -> list[tuple[Food, float]]:
        query_vector = embeddings.encode(
            f"query: {name}", 
            normalize_embeddings=True
        ).tolist()

        with SessionLocal() as session:
            distance_func = Food.embedding.cosine_distance(query_vector)

            results = (
                session.query(Food, distance_func.label("distance"))
                .filter(Food.is_deleted == False)
                .order_by(distance_func)
                .options(joinedload(Food.servings))
                .limit(k)
                .all()
            )
            return results
        
    @staticmethod
    def find_many_by_ids(ids: list[int]) -> list[Food]:
        with SessionLocal() as session:
            return (
                session.query(Food)
                .filter(Food.id.in_(ids), Food.is_deleted == False)
                .options(joinedload(Food.servings))
                .all()
            )