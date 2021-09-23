from flask import request, jsonify, redirect, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import User, AnimeData, Recommended
from sqlalchemy import desc
from src.settings import ENV_VALUES
from src.utils import img_encode

app = Blueprint("recent", __name__)
api = Api(app)


class RecentRecommend(Resource):
    # recommendされた最近のアニメを取得する
    # [GET] : "num": intに変換可能なstring, "sessionID": セッションID
    # {'animes': [ {"image": base64(string), "id": int}]} が返る
    def post(self):
        if request.method == "POST":
            image_num = request.json["num"]
            session_id = request.json["sessionID"]
            user = User.query.filter(User.session_id == session_id).first()
            if user is not None:
                # recommendedの日付データを見て新しい順に持ってくれば良い.
                # recommendedとAnimeDataをanime_idでjoinして, user_idを指定して時刻順にとってきて数の上限を設定する.
                past_data = (
                    db.session.query(Recommended, AnimeData)
                    .join(Recommended, AnimeData.anime_id == Recommended.anime_id)
                    .filter(Recommended.user_id == user.user_id)
                    .order_by(desc(Recommended.updated_at))
                    .limit(int(image_num))
                    .all()
                )
                if past_data is None:
                    response_data = {"animes": []}
                else:
                    # 返すデータがある場合
                    # print([data[1].anime_id for data in past_data])
                    # 各データのimageプロパティから画像をbase64でエンコードしたものを辞書にして返す.
                    response_data = {
                        "animes": [
                            {
                                "image": img_encode(data[1].image),
                                "id": data[0].anime_id,
                            }
                            for data in past_data
                        ]
                    }
                return jsonify(response_data)
            else:
                return redirect(ENV_VALUES["APP_URL"])


api.add_resource(RecentRecommend, "/recent")
