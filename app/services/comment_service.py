from datetime import datetime, timezone
from werkzeug.exceptions import NotFound
from app.extensions import sentiment_analyzer
from app.models import Comment
from app.repositories import RecipeRepository, CommentRepository
from app.schemas.recipe_comment_schema import CommentsListQueryParams, CreateRecipeCommentSchema
from app.utils.database import db_commit

class CommentService:

    @staticmethod
    def create_recipe_comment(recipe_id: int, user_id: int, data: CreateRecipeCommentSchema):
        # Validate recipe existence
        recipe = RecipeRepository.find_by_id(recipe_id)
        if not recipe:
            raise NotFound("Recipe not found")
        
        # Analyze sentiment
        sentiment = sentiment_analyzer.analyze(data.comment)
        
        # Create comment object
        new_comment = Comment(
            recipe_id=recipe_id,
            user_id=user_id,
            text=data.comment,
            sentiment=sentiment,
        )
        
        # Save the comment
        CommentRepository.save(new_comment)
        db_commit()

        return {
            "id": new_comment.id,
            "recipe_id": new_comment.recipe_id,
            "user_id": new_comment.user_id,
            "user_name": new_comment.user.name,
            "comment": new_comment.text,
            "sentiment": new_comment.sentiment,
            "created_at": new_comment.created_at.isoformat()
        }
    
    @staticmethod
    def get_recipe_comments(recipe_id: int, user_id: int, params: CommentsListQueryParams):
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
                "id": last.id
            }

        has_more = len(comments) == params.limit

        return results, {
            "next_cursor": next_cursor,
            "has_more": has_more
        }
    
    @staticmethod
    def delete_recipe_comment(comment_id: int, user_id: int):
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
        db_commit()

        return
    