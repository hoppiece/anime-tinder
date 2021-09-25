from flask import request, redirect, jsonify, Blueprint
from flask_restful import Resource, Api
from src.database import db
from src.models import User
from requests_oauthlib import OAuth1Session
from src.settings import ENV_VALUES
from urllib.parse import parse_qsl
import json
import hashlib
import re


app = Blueprint("callback", __name__)
api = Api(app)


class Callback(Resource):
    def get(self):
        # twitter api key
        consumer_api_key = ENV_VALUES["CONSUMER_API_KEY"]
        consumer_secret_key = ENV_VALUES["CONSUMER_SECRET_KEY"]
        access_token_url = "https://api.twitter.com/oauth/access_token"
        users_show_url = "https://api.twitter.com/1.1/users/show.json"
        # get_timeline_url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
        try:
            # getパラメータを取得
            oauth_token = request.args.get("oauth_token")
            oauth_verifier = request.args.get("oauth_verifier")
            # リクエストトークン取得から返ってきたgetパラメータを用いてアクセストークンを取得.
            # 失敗したら認証のときと同様にリダイレクト
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
                    user = users[0]
                    print(f"hello, {user.name}")  # デバッグ用出力
                    user.session_id = session_id
                    db.session.commit()
                db.session.close()

                # アイコン画像URLから_normalを取り除きオリジナルサイズのものを得ている.
                # https://syncer.jp/Web/API/Twitter/Snippet/4/
                image_url = re.sub(r"_normal", "", user_data["profile_image_url_https"])
                # 返すデータを整えてjsonで返す
                response_data = {
                    "sessionId": session_id,
                    "username": access_token["screen_name"],
                    "profile_image_url": image_url,
                }
                return jsonify(response_data)
            else:
                raise Exception(
                    f"response status code is not 200 (but {response.status_code})"
                )
        except Exception as e:
            print(e)
            return redirect(ENV_VALUES["APP_URL"])


api.add_resource(Callback, "/callback")
