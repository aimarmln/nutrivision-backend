import uuid
from sqlalchemy.orm import joinedload
from app.database import SessionLocal
from app.models.comment import Comment

class CommentRepository:

    @staticmethod
    def find_by_recipe_id(recipe_id: uuid.UUID) -> list[Comment]:
        with SessionLocal() as session:
            return (
                session.query(Comment)
                .options(joinedload(Comment.user))
                .filter(Comment.recipe_id == recipe_id)
                .all()
            )
    
    @staticmethod
    def save(comment: Comment) -> Comment:
        with SessionLocal() as session:
            session.add(comment)
            session.commit()          
            session.refresh(comment)  
            return comment
    