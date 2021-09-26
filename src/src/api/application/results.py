from flask import request, jsonify, redirect, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import User, LikeUnlike, AnimeData, Recommended
from sqlalchemy import desc
from src.settings import ENV_VALUES
from src.utils import img_encode, collaborative_filtering

app = Blueprint("rslts", __name__)
api = Api(app)


class Results(Resource):
    # likeunlikeステータスを受け取り、過去の情報をもとにおすすめの情報を返す.
    # [POST] : {"sessionID": セッションID, "animes": [{"animeId": string, "like", int}, ...]}
    # {
    #    'animes': [
    #        {
    #           "id": int,
    #           "title": string,
    #           "image": base64(string),
    #           "description",
    #           "genre": [string, string, ...]
    #           "company": string
    #        }
    #    ]
    # }
    # が返る
    def post(self):
        if request.method == "POST":
            # テスト用クエリ（これをターミナルで打ち込むとpostでjsonが送信されます. データベースにも反映されるはずです）
            # curl http://localhost:5000/app/rslts -X\
            # POST -H "Content-Type: application/json"\
            # --data '{"sessionID": "value", "animes": [{"animeId": "4", "like": "0"},\
            #  {"animeId": "5", "like": "2"}]}'

            session_id = request.json["sessionID"]
            request_body = request.json["animes"]
            # 送られてきたアニメidとstatusのリストを並べた二次元リストに展開しておく.
            all_ul_data = [
                [int(anime["animeId"]), int(anime["like"])] for anime in request_body
            ]

            # テストするときはパラメータが無いので他で適当にfilter
            user = User.query.filter(User.session_id == session_id).first()
            # user = User.query.filter(User.name == "your_twitter_id").first()
            if user is not None:
                try:
                    for ul_data in all_ul_data:
                        # like_unlikeの登録をする. 過去に同じuserとanime_idに対して登録があれば, それを更新する.
                        past_ul = (
                            LikeUnlike.query.filter(LikeUnlike.user_id == user.user_id)
                            .filter(LikeUnlike.anime_id == ul_data[0])
                            .first()
                        )
                        if past_ul is not None:
                            # 過去に登録されたものがあれば更新
                            past_ul.status = ul_data[1]
                        else:
                            # Noneなら追加
                            like_unlike = LikeUnlike(
                                user_id=user.user_id,
                                anime_id=ul_data[0],
                                status=ul_data[1],
                            )
                            db.session.add(like_unlike)
                        db.session.commit()
                    # 登録が終わったら今回受け取った情報でlike以上のものを一つ選び、レコメンドアルゴリズムに渡す.
                    # like以上が一つでもあるならsuperlikeなものを探してそちらを優先する. なければlikeを取得, なければempty.
                    like_anime_data = [
                        anime_data[0] for anime_data in all_ul_data if anime_data[1] > 0
                    ]
                    if len(like_anime_data) > 0:
                        superlike_anime_data = [
                            anime_data[0]
                            for anime_data in all_ul_data
                            if anime_data[1] == 2
                        ]
                        if len(superlike_anime_data) > 0:
                            like_anime_id = superlike_anime_data[0]
                        else:
                            like_anime_id = like_anime_data[0]
                    else:
                        raise Exception("like_anime_data is empty")
                    # 今までにlike/unlikeを押したことのある全てのanime_idを取得する. 渡すとき0-indexにしたいので-1しておく.
                    past_ul_data = LikeUnlike.query.filter(
                        LikeUnlike.user_id == user.user_id
                    ).all()
                    past_ul_list = [data.anime_id - 1 for data in past_ul_data]

                    # 今はリストのargが返ってくるので+1してアニメidに直す.
                    recommend = collaborative_filtering(like_anime_id, past_ul_list) + 1

                    # recommendがidなので、その情報を返す. 一つだけとってくる
                    anime = (
                        db.session.query(AnimeData)
                        .filter(AnimeData.anime_id == recommend)
                        .first()
                    )
                    # 該当アニメがないなら例外でエラー
                    if anime is None:
                        raise Exception("anime data not found")

                    # recommendedに登録する. 既存なら何もしない.
                    past_recommend = (
                        Recommended.query.filter(Recommended.user_id == user.user_id)
                        .filter(Recommended.anime_id == recommend)
                        .first()
                    )
                    if past_recommend is None:
                        # Noneなら追加
                        recommended_anime = Recommended(
                            user_id=user.user_id, anime_id=recommend
                        )
                        db.session.add(recommended_anime)
                        db.session.commit()
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
                except Exception as e:
                    # 例外を受け取ったらRecommendedの直近を返すことにする.
                    print(e)
                    anime = (
                        db.session.query(Recommended, AnimeData)
                        .join(Recommended, AnimeData.anime_id == Recommended.anime_id)
                        .filter(Recommended.user_id == user.user_id)
                        .order_by(desc(Recommended.updated_at))
                        .first()[1]
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
        pass


api.add_resource(Results, "/rslts")
