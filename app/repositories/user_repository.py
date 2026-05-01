from app.database import db_session
from app.models import User


class UserRepository:
    
    @staticmethod
    def find_by_id(id: int) -> User | None:
        query = db_session.query(User).filter(
            User.id == id, User.is_deleted == False
        )

        return query.first()
    
    @staticmethod
    def find_by_email(email: str) -> User | None:
        query =  db_session.query(User).filter(
            User.email == email, User.is_deleted == False
        )

        return query.first()

    @staticmethod
    def save(user: User):
        db_session.add(user)
        db_session.flush()
