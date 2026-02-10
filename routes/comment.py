from flask import Blueprint, request, jsonify
from models.comment import Comment
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from utils.comment import analyze_sentiment

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/', methods=['POST'])
@jwt_required()
def add_comment():
    data = request.get_json()
    user_id = get_jwt_identity()
    recipe_id = data.get('recipe_id')
    text = data.get('text')
    sentiment = analyze_sentiment(text)

    comment = Comment(user_id=user_id, recipe_id=recipe_id, text=text, sentiment=sentiment)
    db.session.add(comment)
    db.session.commit()

    return jsonify({'msg': 'Comment added successfully'}), 201
