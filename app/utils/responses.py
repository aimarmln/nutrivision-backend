from flask import jsonify

def success_response(data=None, message="Success", pagination=None, status_code=200):
    """ Generate a standardized success response."""
    response = {
        "status": "success",
        "message": message,
        "data": data
    }

    # Include pagination info if provided
    if pagination is not None:
        response["pagination"] = pagination

    return jsonify(response), status_code


def error_response(message="Error", status_code=400):
    """ Generate a standardized error response."""
    return jsonify({
        "status": "error",
        "message": message,
        "data": None
    }), status_code
