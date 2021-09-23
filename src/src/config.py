# 環境変数を使う場合はosをインポートする
# import os
from src.settings import ENV_VALUES

"""flaskのappのconfig設定オブジェクトを書く"""


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"
    ).format(
        **{
            # 'user': os.getenv('DB_USER', 'root'),
            # "user": "root",
            "user": ENV_VALUES["DB_USER"],
            # 'password': os.getenv('DB_PASSWORD', 'root'),
            # "password": "root",
            "password": ENV_VALUES["DB_PW"],
            # docker network で該当のものを探し,
            # docker network inspect [entrypoint]
            # で出てくる表示のContainersのNameがdbっぽいもののIPv4Addressを記述する.
            # 現在はdocker-composeのnetwork設定により固定化している.
            # 'host': os.getenv('DB_HOST', '172.26.0.2'),
            # "host": "172.30.0.2",
            "host": ENV_VALUES["DB_HOST"],
            # 'database': os.getenv('DB_DATABASE', 'anime_recommender')
            # "database": "anime_recommender",
            "database": ENV_VALUES["DB_NAME"],
        }
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False


Config = DevelopmentConfig
