from flask import Blueprint, request, jsonify
from models.user import User
from extensions import db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import check_password_hash
from utils.user import generate_user_data

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    user_data, calories_per_day = generate_user_data(data)

    new_user = User(**user_data)
    db.session.add(new_user)    
    db.session.commit()

    access_token = create_access_token(identity=str(new_user.id))
    refresh_token = create_refresh_token(identity=str(new_user.id))

    return jsonify({
        'msg': str(calories_per_day),
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 201

@auth_bp.route('/check-email', methods=['POST'])
def checkEmail():
    data = request.get_json()
    email = data.get('email')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'exists': True, 'msg': 'Email is already taken'}), 200
    else:
        return jsonify({'exists': False, 'msg': 'Email is available'}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Invalid password'}), 401

    access_token = create_access_token(identity=str(user.id))
    refresh_token = create_refresh_token(identity=str(user.id))

    return jsonify({
        'msg': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token
    }), 200

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)
    new_refresh_token = create_refresh_token(identity=current_user)

    return jsonify({
        'msg': 'Token refreshed successfully',
        'access_token': new_access_token,
        'refresh_token': new_refresh_token
    }), 200
