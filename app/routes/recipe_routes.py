from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest
from app.services import RecipeService, CommentService
from app.schemas.recipe_comment_schema import CommentsListQueryParams, CreateRecipeCommentSchema
from app.schemas.recipe_schema import RecipesListQueryParams
from app.utils.responses import success_response

recipe_bp = Blueprint('recipes', __name__, url_prefix='/api/recipes')

@recipe_bp.route('', methods=[HTTPMethod.GET])
@jwt_required()
def get_recipes_list():
    # Validate query parameters
    params = RecipesListQueryParams(**request.args)

    # Call service to get all recipes
    result, pagination = RecipeService.get_all_recipes(params)

    return success_response(
        data=result,
        pagination=pagination,
        message='Recipes retrieved successfully',
        status_code=HTTPStatus.OK
    )

@recipe_bp.route('/<int:recipe_id>', methods=[HTTPMethod.GET])
@jwt_required()
def get_recipe_detail(recipe_id: int):
    # Validate recipe ID
    if recipe_id <= 0:
        return BadRequest('Invalid recipe ID. Must be a positive integer.')

    # Call service to get recipe detail
    result = RecipeService.get_recipe_detail(recipe_id)

    return success_response(
        data=result,
        message='Recipe detail retrieved successfully',
        status_code=HTTPStatus.OK
    )

@recipe_bp.route('/<int:recipe_id>/comments', methods=[HTTPMethod.GET])
@jwt_required()
def get_recipe_comments(recipe_id: int):
    # Validate recipe ID
    if recipe_id <= 0:
        return BadRequest('Invalid recipe ID. Must be a positive integer.')
    # Validate query parameters
    params = CommentsListQueryParams(**request.args)
    
    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Call service to get recipe comments
    data, pagination = CommentService.get_recipe_comments(recipe_id, user_id, params)

    return success_response(
        data=data,
        pagination=pagination,
        message='Recipe comments retrieved successfully',
        status_code=HTTPStatus.OK
    )

@recipe_bp.route('/<int:recipe_id>/comments', methods=[HTTPMethod.POST])
@jwt_required()
def create_recipe_comment(recipe_id: int):
    # Validate recipe ID
    if recipe_id <= 0:
        return BadRequest('Invalid recipe ID. Must be a positive integer.')
    
    # Validate request payload
    raw_data = request.get_json()
    validated_data = CreateRecipeCommentSchema(**raw_data)

    # Get user ID from JWT
    user_id = get_jwt_identity()

    # Call service to get recipe detail
    result = CommentService.create_recipe_comment(recipe_id, user_id, validated_data)

    return success_response(
        data=result,
        message='Recipe comment created successfully',
        status_code=HTTPStatus.CREATED
    )
    