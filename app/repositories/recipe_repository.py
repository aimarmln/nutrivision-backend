import uuid
from sqlalchemy import func, and_
from app.database import SessionLocal
from app.models.recipe import Recipe
from app.models.comment import Comment
from app.constants.comment import Sentiment

class RecipeRepository:

    @staticmethod
    def find_by_id(recipe_id: uuid.UUID) -> Recipe | None:
        with SessionLocal() as session:
            return (
                session.query(Recipe)
                .filter(Recipe.id == recipe_id, Recipe.is_deleted == False)
                .first()
            )
    
    @staticmethod
    def find_all() -> list[Recipe]:
        with SessionLocal() as session:
            return (
                session.query(Recipe)
                .filter(Recipe.is_deleted == False)
                .all()
            )
    
    @staticmethod
    def find_all_with_positive_comment_count(search_query: str | None = None) -> list[tuple[Recipe, int]]:
        with SessionLocal() as session:
            query = (
                session.query(
                    Recipe,
                    func.count(Comment.id).label("positive_comment_count")
                )
                .outerjoin(
                    Comment,
                    and_(
                        Comment.recipe_id == Recipe.id,
                        Comment.sentiment == Sentiment.POSITIVE,
                        Comment.is_deleted == False
                    )
                )
                .group_by(Recipe.id)
            )

            if search_query:
                query = query.filter(Recipe.name.ilike(f"%{search_query}%"))

            return query.all()