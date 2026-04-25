import uuid
from sqlalchemy.orm import joinedload
from app.database import SessionLocal
from app.models.serving import Serving
from app.extensions import embeddings

class ServingRepository:

    @staticmethod
    def find_by_id(id: uuid.UUID) -> Serving | None:
        with SessionLocal() as session:
            return (
                session.query(Serving)
                .filter(Serving.id == id, Serving.is_deleted == False)
                .first()
            )
        
    @staticmethod
    def find_many_by_ids(ids: list[uuid.UUID]) -> list[Serving]:
        with SessionLocal() as session:
            return (
                session.query(Serving)
                .filter(Serving.id.in_(ids))
                .all()
            )
        
    @staticmethod
    def get_food_servings(food_id: str, serving: str) -> list[tuple[Serving, float]]:
        query_vector = embeddings.encode(serving, normalize_embeddings=True).tolist()

        with SessionLocal() as session:
            # Buat variabel untuk menampung fungsi jarak
            distance_func = Serving.embedding.cosine_distance(query_vector)

            # Query Serving sekaligus label-kan hasil jaraknya
            results = (
                session.query(Serving, distance_func.label("distance"))
                .filter(Serving.food_id == food_id, Serving.is_deleted == False)
                .order_by(distance_func)
                .options(joinedload(Serving.food))
                .limit(10)
                .all()
            )
            return results # Sekarang berisi list of tuples: (Serving, distance)
    