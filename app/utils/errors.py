from http import HTTPStatus
from app.utils.responses import error_response
from app.utils.logger import logger
from app.database import db_session

# Auth JWT errors
def handle_expired_token(jwt_header, jwt_payload):
    logger.warning("Expired token used", exc_info=True)
    return error_response(
        message="Token has expired",
        status_code=HTTPStatus.UNAUTHORIZED
    )

def handle_invalid_token(error):
    logger.warning("Invalid token", exc_info=True)
    return error_response(
        message="Invalid token",
        status_code=HTTPStatus.UNAUTHORIZED
    )

def handle_missing_token(error):
    logger.warning("Missing token", exc_info=True)

    return error_response(
        message="Authorization token is missing",
        status_code=HTTPStatus.UNAUTHORIZED
    )

# Other errors
def handle_validation_error(e):
    logger.warning('Validation error', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Request body validation error')
    return error_response(
        message=message,
        status_code=HTTPStatus.BAD_REQUEST
    )

def handle_bad_request(e):
    logger.warning('Bad request error', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Bad request')
    return error_response(
        message=message,
        status_code=HTTPStatus.BAD_REQUEST
    )

def handle_not_found(e):
    logger.warning('Resource not found', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Resource not found')
    return error_response(
        message=message,
        status_code=HTTPStatus.NOT_FOUND
    )

def handle_forbidden(e):
    logger.warning('Forbidden access attempt', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Forbidden')
    return error_response(
        message=message,
        status_code=HTTPStatus.FORBIDDEN
    )

def handle_conflict(e):
    logger.warning('Conflict error', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Conflict')
    return error_response(
        message=message,
        status_code=HTTPStatus.CONFLICT
    )

def handle_unauthorized(e):
    logger.warning('Unauthorized access attempt', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Unauthorized')
    return error_response(
        message=message,
        status_code=HTTPStatus.UNAUTHORIZED
    )

def handle_internal_error(e):
    logger.error('Internal server error', exc_info=True)
    db_session.rollback()

    message = getattr(e, 'description', 'Internal server error')
    return error_response(
        message=message,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )
