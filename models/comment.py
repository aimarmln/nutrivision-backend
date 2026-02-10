from extensions import db
from datetime import datetime, timezone

class Comment(db.Model):
    __tablename__ = 'comments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)

    text = db.Column(db.Text, nullable=False)
    sentiment = db.Column(db.Enum(
        'Positive', 'Negative',
        name='sentiment_enum'
    ), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    recipe = db.relationship('Recipe', backref=db.backref('comments', lazy=True))
