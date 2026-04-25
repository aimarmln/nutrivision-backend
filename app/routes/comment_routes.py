
from http import HTTPStatus, HTTPMethod
from flask import Blueprint
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest
from app.services.comment_service import CommentService
from app.utils.responses import success_response

comment_bp = Blueprint('comments', __name__, url_prefix='/api/comments')

@comment_bp.route('/<int:comment_id>', methods=[HTTPMethod.DELETE])
@jwt_required()
def delete_comment(comment_id: int):
    # Validate comment ID
    if comment_id <= 0:
        return BadRequest('Invalid comment ID. Must be a positive integer.')

    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Call service to delete comment
    CommentService.delete_recipe_comment(comment_id, user_id)

    return success_response(
        message='Comment deleted successfully',
        status_code=HTTPStatus.OK
    )
