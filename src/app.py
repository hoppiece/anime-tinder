from flask import Flask, request, jsonify, redirect, url_for, session
import json
import hashlib
import re
from src.database import init_db, db
from src.models import User, LikeUnlike, AnimeData, Recommended
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from flask_cors import CORS
from src.settings import ENV_VALUES
from src.utils import img_encode
from sqlalchemy import desc, asc  # , distinct
import numpy as np
from typing import List

# https://qiita.com/AndanteSysDes/items/a25acc1523fa674e7eda
# https://qiita.com/shirakiya/items/0114d51e9c189658002e
# https://qiita.com/kai_kou/items/5d73de21818d1d582f00
# https://qiita.com/voygerrr/items/4c78d156fc91111798d5


def create_app():
    # twitter api key
    consumer_api_key = ENV_VALUES["CONSUMER_API_KEY"]
    consumer_secret_key = ENV_VALUES["CONSUMER_SECRET_KEY"]
    # Twitter api URLs
    request_token_url = "https://api.twitter.com/oauth/request_token"
    authorization_url = "https://api.twitter.com/oauth/authorize"
    access_token_url = "https://api.twitter.com/oauth/access_token"
    # get_timeline_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

    app = Flask(__name__)
    app.config.from_object("src.config.Config")  # configを別ファイルのオブジェクトから読み込む
    CORS(app)

    app.secret_key = b"\x17x\xf0\x83\x93i\x14\xa3\xec<7\x88A\xca\xb5G"

    init_db(app)  # databaseの初期化を行う

    @app.route("/")
    def index():
        if "user_name" in session:
            # セッション変数の取得
            name = session["user_name"]
            return f"hello {name}"
        else:
            return redirect(url_for("get_twitter_request_token"))

    # 認証画面を返す
    @app.route("/user/login", methods=["GET"])
    def get_twitter_request_token():
        try:
            # リクエストトークンを取得し, 認証urlを取得してリダイレクトする. 失敗したらトップページへのリンクを提示する.
            # oauth_callback = ENV_VALUES['APP_URL']+"/callback"
            twitter = OAuth1Session(consumer_api_key, consumer_secret_key)
            twitter.fetch_request_token(request_token_url)
            auth_url = twitter.authorization_url(authorization_url)
            return redirect(auth_url)

        except Exception as e:
            print(e)
            return redirect(ENV_VALUES["APP_URL"])

    @app.route("/user/callback", methods=["GET"])
    def callback():
        users_show_url = "https://api.twitter.com/1.1/users/show.json"
        try:
            # getパラメータを取得
            oauth_token = request.args.get("oauth_token")
            oauth_verifier = request.args.get("oauth_verifier")
            # リクエストトークン取得から返ってきたgetパラメータを用いてアクセストークンを取得. 失敗したら認証のときと同様
            twitter = OAuth1Session(
                consumer_api_key, consumer_secret_key, oauth_token, oauth_verifier
            )
            response = twitter.post(
                access_token_url, params={"oauth_verifier": oauth_verifier}
            )
            access_token = dict(parse_qsl(response.content.decode("utf-8")))

            twitter = OAuth1Session(
                consumer_api_key,
                consumer_secret_key,
                access_token["oauth_token"],
                access_token["oauth_token_secret"],
            )
            response = twitter.get(
                users_show_url, params={"user_id": access_token["user_id"]}
            )

            if response.status_code == 200:
                user_data = json.loads(response.text)
                # ユーザー登録とセッション情報の兼ね合いがどうなるか未定なのでこのようにしておく
                users = User.query.filter(
                    User.name == access_token["screen_name"]
                ).all()
                # users = User.query.filter(User.user_id==access_token['user_id']).all()

                # セッションID生成
                session_id = hashlib.sha256(
                    access_token["oauth_token"].encode("utf-8")
                ).hexdigest()
                if len(users) == 0:
                    # 存在しないなら登録処理
                    user = User(name=user_data["screen_name"], session_id=session_id)
                    db.session.add(user)
                    db.session.commit()
                else:
                    # print(f"hello, {users[0].name}")
                    # user = User.query.filter(
                    #   User.name==access_token['screen_name']
                    # ).first()
                    user = users[0]
                    print(f"hello, {user.name}")
                    user.session_id = session_id
                    db.session.commit()
                db.session.close()

                # アイコン画像URLから_normalを取り除きオリジナルサイズのものを得ている.
                # https://syncer.jp/Web/API/Twitter/Snippet/4/
                image_url = re.sub(r"_normal", "", user_data["profile_image_url_https"])
                # 返すデータを整えてjsonでreturn
                response_data = {
                    "sessionId": session_id,
                    "username": access_token["screen_name"],
                    "profile_image_url": image_url,
                }
                # print(session)
                return jsonify(response_data)
            else:
                raise Exception(
                    f"response status code is not 200 (is {response.status_code})"
                )
        except Exception as e:
            print(e)
            return redirect(ENV_VALUES["APP_URL"])

    @app.route("/user/logout", methods=["GET"])
    def logout():
        session_id = request.args.get("sessionID")
        user = User.query.filter(User.session_id == session_id).first()
        if user is not None:
            user.session_id = None
            db.session.commit()
        return redirect(ENV_VALUES["APP_URL"])

    # recommendされた最近のアニメを取得する
    # [GET] : "num": intに変換可能なstring, "sessionID": セッションID
    # {'animes': [ {"image": base64(string), "id": int}]} が返る
    @app.route("/user/recent", methods=["POST"])
    def fetch_recent_user_data():
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
    @app.route("/app/recs", methods=["POST"])
    def fetch_random_anime_data():
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
            # user = User.query.filter(User.name == "Kw_I_KU").first()
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

    def user_anime_matrix():
        # user_idとanime_idを縦横にもち値がstatusの二次元配列を返す
        all_users = User.query.all()
        anime_num = len(AnimeData.query.all())
        user_id_list = [user.user_id for user in all_users]
        print("user_id_list:", user_id_list)
        res = []
        for user_id in user_id_list:
            # ユーザーひとりに対してアニメに対するlikeunlikeのstatusを取得, リストで保持する.
            lu_data = (
                db.session.query(LikeUnlike)
                .filter(LikeUnlike.user_id == user_id)
                .order_by(asc(LikeUnlike.anime_id))
                .all()
            )

            if lu_data is not None:
                # そのユーザーがlike_unlikeを一つでも設定しているなら
                user_status_list = []
                index = 1  # user_status_listの要素数は最終的にanime_numにならないといけないのでそのようにする
                for data in lu_data:
                    data_anime_id = data.anime_id
                    data_status = data.status
                    # 前のループの次の場所からこのループのanime_idの場所まで0で埋める（デフォルト値）
                    user_status_list.extend([0] * (data_anime_id - index))
                    # このループのデータをいれる
                    user_status_list.append(data_status)
                    # インデックスを更新する
                    index = data_anime_id + 1
                # 終わったら最後までを0で埋める.
                user_status_list.extend([0] * (anime_num + 1 - index))
            else:
                # 一つもlike_unlikeをしていないなら全て0で埋める
                user_status_list = [0] * anime_num
            res.append(user_status_list)
        # return jsonify(res) # 確認用
        # アニメID順にステータスが並んだリストがユーザーごとに並んでいる二次元リストを返す.
        return res

    def anime_similarity():
        content_lu = np.array(user_anime_matrix()).T
        # anime_num, user_num = content_lu.shape[0], content_lu.shape[1]
        corr_mat = np.dot(content_lu, content_lu.T)
        anime_norm_vec = np.linalg.norm(content_lu, axis=1)
        anime_norm_mat = np.outer(anime_norm_vec, anime_norm_vec)
        anime_norm_mat = np.where(
            np.absolute(anime_norm_mat) < 0.001, anime_norm_mat, 1
        )
        cos_sim_mat = corr_mat / anime_norm_mat
        cos_sim_mat = cos_sim_mat - np.diag(cos_sim_mat, k=0)
        return cos_sim_mat

    def collaborative_filtering(ith_anime: int, liked_anime_list: List[int]) -> int:
        # i 番目のアニメに対して、コサイン類似度ベースの協調フィルタリングでレコメンドされたアニメのid を返します。
        # 既にlike 済みのアニメは無視します
        cos_sim_mat = anime_similarity()
        recommend_vec = cos_sim_mat[ith_anime]
        recommend_vec[liked_anime_list] = 0
        recommend_id = np.argmax(recommend_vec)
        return recommend_id

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
    @app.route("/app/rslts", methods=["POST"])
    def anime_results():
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
            # user = User.query.filter(User.name == "Kw_I_KU").first()
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

    @app.route("/app/fetch", methods=["POST"])
    def fetch_anime_data():
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

    return app


app = create_app()
