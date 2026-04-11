import uuid
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.database import SessionLocal
from app.models.comment import Comment
from app.constants.comment import Sentiment

class CommentRepository:

    @staticmethod
    def find_by_id(comment_id: uuid.UUID) -> Comment | None:
        with SessionLocal() as session:
            return (
                session.query(Comment)
                .filter(Comment.id == comment_id, Comment.is_deleted == False)
                .first()
            )

    @staticmethod
    def find_by_recipe_id(
        recipe_id: uuid.UUID,
        last_created_at: datetime | None = None,
        limit: int = 20
    ) -> list[Comment]:
        with SessionLocal() as session:
            query = session.query(Comment).options(joinedload(Comment.user)).filter(
                Comment.recipe_id == recipe_id,
                Comment.is_deleted == False
            )

            if last_created_at:
                query = query.filter(Comment.created_at < last_created_at)

            return (
                query.order_by(Comment.created_at.desc())
                .limit(limit)
                .all()
            )
        
    @staticmethod
    def count_positive_comments_by_recipe_id(recipe_id: uuid.UUID) -> int:
        with SessionLocal() as session:
            return (
                session.query(func.count(Comment.id))
                .filter(
                    Comment.recipe_id == recipe_id,
                    Comment.sentiment == Sentiment.POSITIVE,
                    Comment.is_deleted == False
                )
                .scalar()
            )
    
    @staticmethod
    def save(comment: Comment) -> Comment:
        with SessionLocal() as session:
            session.add(comment)
            session.commit()          
            session.refresh(comment)  

            comment = session.query(Comment)\
                .options(joinedload(Comment.user))\
                .filter(Comment.id == comment.id)\
                .first()

            return comment
    