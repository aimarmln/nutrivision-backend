import uuid
from app.database import SessionLocal
from app.models.serving import Serving

class ServingRepository:

    @staticmethod
    def find_by_id(id: uuid.UUID) -> Serving | None:
        with SessionLocal() as session:
            return (
                session.query(Serving)
                .filter(Serving.id == id, Serving.is_deleted == False)
                .first()
            )
    