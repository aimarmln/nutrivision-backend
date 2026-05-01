from http import HTTPStatus
from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from werkzeug.exceptions import BadRequest
from app.schemas.chat_schema import ChatMessagesQueryParams, ChatSchema, SessionsListQueryParams
from app.services import ChatService
from app.utils.responses import success_response

chat_bp = Blueprint('chat', __name__, url_prefix='/api/chat')

@chat_bp.route("", methods=["POST"])
@jwt_required()
def create_chat():
    data = ChatSchema(**request.get_json())

    user_id = int(get_jwt_identity())

    result = ChatService.create_chat(
        user_id=user_id,
        message=data.message
    )

    return success_response(
        data=result,
        message='Chat session created successfully',
        status_code=HTTPStatus.CREATED
    )

@chat_bp.route("", methods=["GET"])
@jwt_required()
def list_chat():
    params = SessionsListQueryParams(**request.args)

    user_id = int(get_jwt_identity())

    results, pagination = ChatService.list_sessions(user_id, params)

    return success_response(
        data=results,
        message='Chat sessions retrieved successfully',
        pagination=pagination,
        status_code=HTTPStatus.OK
    )

@chat_bp.route("/<int:session_id>", methods=["POST"])
@jwt_required()
def send_message(session_id: int):
    if session_id <= 0:
        return BadRequest('Invalid session ID. Must be a positive integer.')
    
    data = ChatSchema(**request.get_json())

    user_id = int(get_jwt_identity())

    result = ChatService.send_message(
        user_id=user_id,
        session_id=session_id,
        message=data.message
    )

    return success_response(
        data=result,
        message='Message sent successfully',
        status_code=HTTPStatus.OK
    )

@chat_bp.route("/<int:session_id>", methods=["GET"])
@jwt_required()
def get_chat(session_id: int):
    if session_id <= 0:
        return BadRequest('Invalid session ID. Must be a positive integer.')
    
    params = ChatMessagesQueryParams(**request.args)

    user_id = int(get_jwt_identity())

    result, pagination = ChatService.get_messages(user_id, session_id, params)

    return success_response(
        data=result,
        message='Messages retrieved successfully',
        pagination=pagination,
        status_code=HTTPStatus.OK
    )

# @chat_bp.route("/foods-embeddings", methods=["POST"])
# def foods_embeddings():
#     raw_data = request.get_json()
#     data = ChatSchema(**raw_data)

#     foods = ChatService.get_foods_by_name(data.message)

#     return success_response(
#         data=foods,
#         message='Chat processed successfully',
#         status_code=HTTPStatus.OK
#     )


# @chat_bp.route("/servings-embeddings", methods=["POST"])
# def servings_embeddings():
#     raw_data = request.get_json()
#     data = TestServingSchema(**raw_data)

#     servings = ChatService.get_food_servings(data.food_id, data.serving)

#     return success_response(
#         data=servings,
#         message='Chat processed successfully',
#         status_code=HTTPStatus.OK
#     )