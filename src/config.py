# 環境変数を使う場合はosをインポートする
# import os

"""flaskのappのconfig設定オブジェクトを書く"""


class DevelopmentConfig:
    SQLALCHEMY_DATABASE_URI = (
        "mysql+pymysql://{user}:{password}" "@{host}/{database}?charset=utf8mb4"
    ).format(
        **{
            # 'user': os.getenv('DB_USER', 'root'),
            "user": "root",
            # 'password': os.getenv('DB_PASSWORD', 'root'),
            "password": "root",
            # docker network で該当のものを探し,
            # docker network inspect [entrypoint]
            # で出てくる表示のContainersのNameがdbっぽいもののIPv4Addressを記述する.
            # 現在はdocker-composeのnetwork設定により固定化している.
            # 'host': os.getenv('DB_HOST', '172.26.0.2'),
            "host": "172.30.0.2",
            # 'database': os.getenv('DB_DATABASE', 'anime_recommender')
            "database": "anime_recommender",
        }
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    JSON_AS_ASCII = False


Config = DevelopmentConfig
