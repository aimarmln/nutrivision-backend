from sqlalchemy.orm import joinedload
from app.database import db_session
from app.models import Serving
from app.extensions import embeddings


class ServingRepository:

    @staticmethod
    def find_by_id(id: int) -> Serving | None:
        query = db_session.query(Serving).filter(
            Serving.id == id, 
            Serving.is_deleted == False
        )

        return query.first()
        
    @staticmethod
    def find_many_by_ids(ids: list[int], preload_food: bool = False) -> list[Serving]:
        query = db_session.query(Serving).filter(
            Serving.id.in_(ids),
            Serving.is_deleted == False
        )

        if preload_food:
            query = query.options(joinedload(Serving.food))

        return query.all()
        
    @staticmethod
    def get_food_servings(
        food_id: int, 
        serving: str
    ) -> list[tuple[Serving, float]]:
        query_vector = embeddings.encode(
            f"query: {serving}", 
            normalize_embeddings=True
        ).tolist()

        distance_func = Serving.embedding.cosine_distance(query_vector)

        query = db_session.query(
            Serving, 
            distance_func.label("distance")
        ).filter(
            Serving.food_id == food_id, 
            Serving.is_deleted == False
        ).order_by(distance_func).options(joinedload(Serving.food)).limit(10)

        return query.all()
    