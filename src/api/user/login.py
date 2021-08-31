from flask import redirect, Blueprint
from flask_restful import Resource, Api
from requests_oauthlib import OAuth1Session
from src.settings import ENV_VALUES

app = Blueprint("login", __name__)
api = Api(app)


# 認証画面を返す
class get_twitter_request_token(Resource):
    def get(self):
        # twitter api key
        consumer_api_key = ENV_VALUES["CONSUMER_API_KEY"]
        consumer_secret_key = ENV_VALUES["CONSUMER_SECRET_KEY"]
        # Twitter api URLs
        request_token_url = "https://api.twitter.com/oauth/request_token"
        authorization_url = "https://api.twitter.com/oauth/authorize"
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


api.add_resource(get_twitter_request_token, "/login")
