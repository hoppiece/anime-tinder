from flask import Flask
from src.api.user import login, callback, logout, recent_recommend
from src.api.application import random_anime, results, fetch_data
from src.database import init_db
from flask_cors import CORS

import src.models  # noqa: #F401

# https://qiita.com/AndanteSysDes/items/a25acc1523fa674e7eda
# https://qiita.com/shirakiya/items/0114d51e9c189658002e
# https://qiita.com/kai_kou/items/5d73de21818d1d582f00
# https://qiita.com/voygerrr/items/4c78d156fc91111798d5
# https://qiita.com/keichiro24/items/c72c57b54332431c67ec


def create_app():
    app = Flask(__name__)
    app.config.from_object("src.config.Config")  # configを別ファイルのオブジェクトから読み込む
    CORS(app)

    app.register_blueprint(login.app, url_prefix="/user")  # 認証画面を返す
    app.register_blueprint(callback.app, url_prefix="/user")  # 認証時のコールバック
    app.register_blueprint(logout.app, url_prefix="/user")  # ログアウト
    app.register_blueprint(recent_recommend.app, url_prefix="/user")  # 直近のレコメンドデータを返す
    app.register_blueprint(random_anime.app, url_prefix="/app")  # 指定した数のアニメデータを返す
    app.register_blueprint(results.app, url_prefix="/app")  # 結果を計算
    app.register_blueprint(fetch_data.app, url_prefix="/app")  # 求められたアニメのデータを返す

    app.secret_key = b"\x17x\xf0\x83\x93i\x14\xa3\xec<7\x88A\xca\xb5G"

    init_db(app)  # databaseの初期化を行う

    # @app.route("/")
    # def index():
    #     return redirect(url_for("get_twitter_request_token"))

    return app


app = create_app()
