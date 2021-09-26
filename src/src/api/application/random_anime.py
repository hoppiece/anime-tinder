from flask import request, jsonify, redirect, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import User, LikeUnlike, AnimeData
from src.settings import ENV_VALUES
from src.utils import img_encode


app = Blueprint("recs", __name__)
api = Api(app)


class FetchRandomAnimeData(Resource):
    # 指定した数(num)だけカードに表示するアニメの情報を取ってくる。DBにアクセスし、過去に表示したカード以外から適当に選んでくる。
    # [POST] : {"num": intに変換可能なstring, "sessionID": string, "animeId": [int, ...]}
    # {
    #    'animes': [
    #        {
    #           "id": int,
    #           "title": string,
    #           "image": base64(string),
    #           "description",
    #           "id": anime_id,
    #           "genre": [string, string, ...]
    #           "company": string
    #        }
    #    ]
    # }
    # が返る
    def post(self):
        if request.method == "POST":
            # テスト用クエリ（これをターミナルで打ち込むとpostでjsonが送信されます. データベースにも反映されるはずです）
            # curl http://localhost:5000//app/recs -X POST\
            # -H "Content-Type: application/json" --data\
            # '{"num": "5", "sessionID": "value", "animeId": [4,7,8,9,10]}'
            image_num = request.json["num"]
            session_id = request.json["sessionID"]
            anime_id_buffer = request.json["animeId"]
            # テストするときはパラメータが無いので他で適当にfilter
            user = User.query.filter(User.session_id == session_id).first()
            # image_num = "5"
            # user = User.query.filter(User.name == "your_twitter_id").first()
            if user is not None:
                lu_data = (
                    db.session.query(LikeUnlike)
                    .filter(LikeUnlike.user_id == user.user_id)
                    .all()
                )
                past_animes = [lu.anime_id for lu in lu_data] + anime_id_buffer
                past_animes = list(set(past_animes))
                # 過去に表示したことがあるものを含まないものからimage_num個に制限してとってくる
                animes = (
                    db.session.query(AnimeData)
                    .filter(AnimeData.anime_id.notin_(past_animes))
                    .limit(int(image_num))
                    .all()
                )
                response_data = {
                    "animes": [
                        {
                            "id": anime.anime_id,
                            "title": anime.title,
                            "image": img_encode(anime.image),  # 画像をbase64で返す
                            "description": anime.description,
                            "year": anime.year,
                            "genre": anime.genre.split(),
                            "company": anime.company,
                        }
                        for anime in animes
                    ]
                }
                return jsonify(response_data)
            else:
                return redirect(ENV_VALUES["APP_URL"])


api.add_resource(FetchRandomAnimeData, "/recs")
