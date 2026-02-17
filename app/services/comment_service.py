import uuid
from werkzeug.exceptions import NotFound
from app.extensions import sentiment_analyzer
from app.models.comment import Comment
from app.repositories.recipe_repository import RecipeRepository
from app.repositories.comment_repository import CommentRepository
from app.schemas.recipe_comment_schema import CreateRecipeCommentSchema

class CommentService:

    @staticmethod
    def create_recipe_comment(recipe_id: uuid.UUID, user_id: uuid.UUID, data: CreateRecipeCommentSchema):
        # Validate recipe existence
        recipe = RecipeRepository.find_by_id(recipe_id)
        if not recipe:
            raise NotFound("Recipe not found")
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze(data.comment)
        
        # Create comment object
        new_comment = Comment(
            id=uuid.uuid4(),
            recipe_id=recipe_id,
            user_id=user_id,
            text=data.comment,
            sentiment=sentiment,
        )
        
        # Save the comment
        saved_comment = CommentRepository.save(new_comment)

        return {
            "id": saved_comment.id,
            "recipe_id": saved_comment.recipe_id,
            "user_id": saved_comment.user_id,
            "comment": saved_comment.text,
            "sentiment": saved_comment.sentiment
        }
    