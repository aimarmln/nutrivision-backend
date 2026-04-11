import uuid
from datetime import datetime, timezone
from werkzeug.exceptions import NotFound
from app.extensions import sentiment_analyzer
from app.models.comment import Comment
from app.repositories.recipe_repository import RecipeRepository
from app.repositories.comment_repository import CommentRepository
from app.schemas.recipe_comment_schema import CommentsListQueryParams, CreateRecipeCommentSchema

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
            "user_name": saved_comment.user.name,
            "comment": saved_comment.text,
            "sentiment": saved_comment.sentiment,
            "created_at": saved_comment.created_at.isoformat()
        }
    
    @staticmethod
    def get_recipe_comments(recipe_id: uuid.UUID, user_id: uuid.UUID, params: CommentsListQueryParams):
        # Retrieve comments for the recipe
        comments = CommentRepository.find_by_recipe_id(
            recipe_id=recipe_id,
            last_created_at=params.last_created_at,
            limit=params.limit
        )

        results = [
            {
                'id': comment.id,
                'name': comment.user.name,
                'text': comment.text,
                'sentiment': comment.sentiment,
                'created_at': comment.created_at.isoformat(),
                'is_own_comment': str(comment.user_id) == str(user_id)
            }
            for comment in comments
        ]

        next_cursor = None
        if comments:
            last = comments[-1]
            next_cursor = {
                "created_at": last.created_at.isoformat(),
                "id": str(last.id)
            }

        has_more = len(comments) == params.limit

        return results, {
            "next_cursor": next_cursor,
            "has_more": has_more
        }
    
    @staticmethod
    def delete_recipe_comment(comment_id: uuid.UUID, user_id: uuid.UUID):
        # Retrieve comment
        comment = CommentRepository.find_by_id(comment_id)
        if not comment:
            raise NotFound("Comment not found")
        
        # Check ownership
        if str(comment.user_id) != str(user_id):
            raise NotFound("Comment not found")  # Hide existence of the comment
        
        # Soft delete the comment
        comment.is_deleted = True
        comment.deleted_at = datetime.now(timezone.utc)

        CommentRepository.save(comment)

        return
    