from datetime import datetime
from requests import session
from sqlalchemy import func
from sqlalchemy.orm import joinedload
from app.database import db_session
from app.models import Comment
from app.constants.comment import Sentiment


class CommentRepository:

    @staticmethod
    def find_by_id(comment_id: int) -> Comment | None:
        query = db_session.query(Comment).filter(
            Comment.id == comment_id, 
            Comment.is_deleted == False
        )

        return query.first()

    @staticmethod
    def find_by_recipe_id(
        recipe_id: int,
        last_created_at: datetime | None = None,
        limit: int = 20
    ) -> list[Comment]:
        query = db_session.query(Comment).filter(
            Comment.recipe_id == recipe_id,
            Comment.is_deleted == False
        ).options(joinedload(Comment.user))

        if last_created_at:
            query = query.filter(
                Comment.created_at < last_created_at
            )

        query = query.order_by(
            Comment.created_at.desc()
        ).limit(limit)

        return query.all()
    
    @staticmethod
    def count_positive_comments_by_recipe_id(recipe_id: int) -> int:
        query = db_session.query(func.count(Comment.id)).filter(
            Comment.recipe_id == recipe_id,
            Comment.sentiment == Sentiment.POSITIVE,
            Comment.is_deleted == False
        )

        return query.scalar()
    
    @staticmethod
    def save(comment: Comment):
        db_session.add(comment)
        db_session.flush()
    