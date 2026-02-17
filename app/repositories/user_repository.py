import uuid
from app.database import SessionLocal
from app.models.user import User

class UserRepository:
    
    @staticmethod
    def find_by_id(id: uuid.UUID) -> User | None:
        with SessionLocal() as session:
            return (
                session.query(User)
                .filter(User.id == id, User.is_deleted == False)
                .first()
            )
        
    @staticmethod
    def find_by_email(email: str) -> User | None:
        with SessionLocal() as session:
            return (
                session.query(User)
                .filter(User.email == email, User.is_deleted == False)
                .first()
            )

    @staticmethod
    def save(user: User) -> User:
        with SessionLocal() as session:
            session.add(user)
            session.commit()
            session.refresh(user)
            return user
