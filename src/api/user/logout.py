from flask import request, redirect, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import User
from src.settings import ENV_VALUES

app = Blueprint("logout", __name__)
api = Api(app)


class Logout(Resource):
    def get(self):
        session_id = request.args.get("sessionID")
        user = User.query.filter(User.session_id == session_id).first()
        if user is not None:
            user.session_id = None
            db.session.commit()
        return redirect(ENV_VALUES["APP_URL"])


api.add_resource(Logout, "/logout")
