from flask import request
from werkzeug.exceptions import BadRequest

def validate_image_upload(field_name: str = 'image'):
    if field_name not in request.files:
        raise BadRequest(f'{field_name} file is required')

    file = request.files[field_name]

    if file.filename.strip() == '':
        raise BadRequest('Filename cannot be empty')

    if not file.mimetype.startswith('image/'):
        raise BadRequest('Uploaded file must be an image')

    return file
