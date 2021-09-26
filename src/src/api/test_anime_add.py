from flask import request, Response, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import AnimeData
import json


app = Blueprint("anime_add", __name__)
api = Api(app)


class Anime(Resource):
    def get(self):
        return "test anime add"

    def post(self):
        # テストの際は
        """
        curl http://localhost:5000/anime_add\
        -X POST -H "Content-Type: application/json"\
        --data '{"title": "title", "image": "path", "description": "desc",\
            "year": "2021", "genre": "genre", "company": "cp"}'
        """
        title = request.json["title"]
        image = request.json.get("image", None)
        desc = request.json["description"]
        year = request.json["year"]
        genre = request.json["genre"]
        company = request.json["company"]
        # ユーザー作成
        new_anime = AnimeData(
            title=title,
            image=image,
            description=desc,
            year=year,
            genre=genre,
            company=company,
        )
        db.session.add(new_anime)
        db.session.commit()
        return Response(
            json.dumps({"message": "アニメを新たに作成しました."}, ensure_ascii=False), status=200
        )


api.add_resource(Anime, "/anime_add")
