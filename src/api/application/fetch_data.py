from flask import request, jsonify, redirect, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import User, AnimeData
from src.settings import ENV_VALUES
from src.utils import img_encode


app = Blueprint("fetch", __name__)
api = Api(app)


# 求められたアニメのデータを返す
class FetchAnimeData(Resource):
    def post(self):
        if request.method == "POST":
            anime_id = request.json["animeId"]
            session_id = request.json["sessionID"]
            user = User.query.filter(User.session_id == session_id).first()
            if user is not None:
                anime = (
                    db.session.query(AnimeData)
                    .filter(AnimeData.anime_id == anime_id)
                    .first()
                )
                if anime is None:
                    response_data = {"animes": []}
                else:
                    response_data = {
                        "animes": [
                            {
                                "id": anime.anime_id,
                                "title": anime.title,
                                "image": img_encode(anime.image),
                                "description": anime.description,
                                "year": anime.year,
                                "genre": anime.genre.split(),
                                "company": anime.company,
                            }
                        ]
                    }
                return jsonify(response_data)
            else:
                return redirect(ENV_VALUES["APP_URL"])


api.add_resource(FetchAnimeData, "/fetch")
