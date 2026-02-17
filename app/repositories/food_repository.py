import uuid
from app.database import SessionLocal
from app.models.food import Food

class FoodRepository:

    @staticmethod
    def find_all(search_query: str | None = None   ) -> list[Food]:
        with SessionLocal() as session:
            query = session.query(Food).filter(Food.is_deleted == False)
            if search_query:
                query = query.filter(Food.name.ilike(f"%{search_query}%"))
            return query.all()

    @staticmethod
    def find_by_id(id: uuid.UUID) -> Food | None:
        with SessionLocal() as session:
            return (
                session.query(Food)
                .filter(Food.id == id, Food.is_deleted == False)
                .first()
            )
        
    @staticmethod
    def find_by_yolo_labels(yolo_labels: list[str]) -> list[Food]:
        with SessionLocal() as session:
            return (
                session.query(Food)
                .filter(
                    Food.yolo_label.in_(yolo_labels),
                    Food.is_deleted == False
                )
                .all()
            )
    