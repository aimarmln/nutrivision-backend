from http import HTTPStatus, HTTPMethod
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.chat_schema import ChatSchema, TestServingSchema
from app.services.chat_service import ChatService
from app.utils.responses import success_response

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route("", methods=["POST"])
@jwt_required()
def chat():
    user_id = get_jwt_identity()

    raw_data = request.get_json()
    data = ChatSchema(**raw_data)

    result = ChatService.chat_ai(
        user_id=user_id,
        message=data.message
    )

    return success_response(
        data=result,
        message='Chat processed successfully',
        status_code=HTTPStatus.OK
    )

@chat_bp.route("/foods-embeddings", methods=["POST"])
def foods_embeddings():
    raw_data = request.get_json()
    data = ChatSchema(**raw_data)

    foods = ChatService.get_foods_by_name(data.message)

    return success_response(
        data=foods,
        message='Chat processed successfully',
        status_code=HTTPStatus.OK
    )


@chat_bp.route("/servings-embeddings", methods=["POST"])
def servings_embeddings():
    raw_data = request.get_json()
    data = TestServingSchema(**raw_data)

    servings = ChatService.get_food_servings(data.food_id, data.serving)

    return success_response(
        data=servings,
        message='Chat processed successfully',
        status_code=HTTPStatus.OK
    )