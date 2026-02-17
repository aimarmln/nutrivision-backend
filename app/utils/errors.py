from http import HTTPStatus
from app.utils.responses import error_response
from app.utils.logger import logger

def handle_validation_error(e):
    logger.warning('Validation error', exc_info=True)
    return error_response(
        message='Request body validation error',
        status_code=HTTPStatus.BAD_REQUEST
    )

def handle_bad_request(e):
    logger.warning('Bad request error', exc_info=True)
    return error_response(
        message=str(e) or 'Bad request',
        status_code=HTTPStatus.BAD_REQUEST
    )

def handle_not_found(e):
    logger.warning('Resource not found', exc_info=True)
    return error_response(
        message=str(e) or 'Resource not found',
        status_code=HTTPStatus.NOT_FOUND
    )

def handle_forbidden(e):
    logger.warning('Forbidden access attempt', exc_info=True)
    return error_response(
        message=str(e) or 'Forbidden',
        status_code=HTTPStatus.FORBIDDEN
    )

def handle_conflict(e):
    logger.warning('Conflict error', exc_info=True)
    return error_response(
        message=str(e) or 'Conflict',
        status_code=HTTPStatus.CONFLICT
    )

def handle_unauthorized(e):
    logger.warning('Unauthorized access attempt', exc_info=True)
    return error_response(
        message=str(e) or 'Unauthorized',
        status_code=HTTPStatus.UNAUTHORIZED
    )

def handle_internal_error(e):
    logger.error('Internal server error', exc_info=True)
    return error_response(
        message='Internal server error',
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR
    )
