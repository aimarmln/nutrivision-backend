from sqlalchemy import func, and_
from app.database import db_session
from app.models import Recipe, Comment
from app.constants.comment import Sentiment


class RecipeRepository:

    @staticmethod
    def find_by_id(recipe_id: int) -> Recipe | None:
        query = db_session.query(Recipe).filter(
            Recipe.id == recipe_id, 
            Recipe.is_deleted == False
        )

        return query.first()
    
    @staticmethod
    def find_all() -> list[Recipe]:
        query = db_session.query(Recipe).filter(
            Recipe.is_deleted == False
        )

        return query.all()
    
    @staticmethod
    def find_all_paginated(
        search_query: str | None = None,
        page: int = 1,
        limit: int = 20,
        include_positive_comment_count: bool = False
    ) -> list[tuple[Recipe, int]]:
        if include_positive_comment_count:
            query = db_session.query(
                Recipe,
                func.count(Comment.id).label("positive_comment_count")
            ).outerjoin(
                Comment,
                and_(
                    Comment.recipe_id == Recipe.id,
                    Comment.sentiment == Sentiment.POSITIVE,
                    Comment.is_deleted == False
                )
            ).group_by(Recipe.id)
        else:
            query = db_session.query(Recipe)

        if search_query:
            query = query.filter(Recipe.name.ilike(f"%{search_query}%"))

        offset_value = (page - 1) * limit

        return query.offset(offset_value).limit(limit).all()
        
    @staticmethod
    def count_all(search_query: str | None = None) -> int:
        query = db_session.query(func.count(Recipe.id)).filter(
            Recipe.is_deleted == False
        )

        if search_query:
            query = query.filter(Recipe.name.ilike(f"%{search_query}%"))

        return query.scalar()
