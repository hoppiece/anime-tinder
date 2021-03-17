from datetime import datetime
from src.database import db

# https://qiita.com/kitarikes/items/9c5d6cbc557ed62bb512

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Unicode(255), nullable=False)
    #email = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)
    user_id = db.Column(db.Unicode(127), nullable=False)

    def __repr__(self):
        return '<User id={id} name={name}>'.format(
                id=self.id, name=self.name)

class AnimeData(db.Model):
    __tablename__ = 'anime_data'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Unicode(255), nullable=False)

class LikeUnlike(db.Model):
    __tablename__ = 'likeunlike'

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    anime_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)