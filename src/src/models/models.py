from datetime import datetime
from src.database import db

# https://qiita.com/kitarikes/items/9c5d6cbc557ed62bb512
# リレーション等がよくわからないのでコメントアウトした.


class User(db.Model):
    __tablename__ = "users"
    __table_args__ = {"extend_existing": True}

    user_id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.Unicode(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
    session_id = db.Column(db.Unicode(255))

    # likeunlike = db.relationship('LikeUnlike', backref='users')

    def __repr__(self):
        return "<User id={id} name={name}>".format(id=self.id, name=self.name)


class AnimeData(db.Model):
    __tablename__ = "anime_data"
    __table_args__ = {"extend_existing": True}

    anime_id = db.Column(db.Integer, primary_key=True, unique=True)
    title = db.Column(db.Unicode(255), nullable=False)
    image = db.Column(db.Unicode(127))
    description = db.Column(db.Text, nullable=False)
    year = db.Column(db.Unicode(127), nullable=False)
    genre = db.Column(db.Unicode(255), nullable=False)
    company = db.Column(db.Unicode(255), nullable=False)

    # likeunlike = db.relationship('LikeUnlike', backref='anime_data')


class LikeUnlike(db.Model):
    __tablename__ = "likeunlike"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    # user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    # anime_id = db.Column(db.Integer,
    #                      db.ForeignKey('anime_data.anime_id'),
    #                      nullable=False
    #                     )
    anime_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )


class Recommended(db.Model):
    __tablename__ = "recommended"
    __table_args__ = {"extend_existing": True}

    id = db.Column(db.Integer, primary_key=True, unique=True)
    user_id = db.Column(db.Integer, nullable=False)
    anime_id = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now
    )
