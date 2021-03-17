from flask import Flask, request, jsonify, render_template, redirect, url_for, session
#from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
import json
import uuid
import re
from src.database import init_db, db
from src.models import User,LikeUnlike,AnimeData
from requests_oauthlib import OAuth1Session
from urllib.parse import parse_qsl
from flask_cors import CORS

# https://qiita.com/AndanteSysDes/items/a25acc1523fa674e7eda
# https://qiita.com/shirakiya/items/0114d51e9c189658002e
# https://qiita.com/kai_kou/items/5d73de21818d1d582f00
# https://qiita.com/voygerrr/items/4c78d156fc91111798d5

def create_app():
    # twitter api key
    consumer_api_key = 'qOoxU6YUCvtlTu59IkrSMwrs7'
    consumer_secret_key = 'QAzP9tbdfUof711fcD7GhiMXJPO5aE3p7GPnVEoZye96pX3XDP'
    # Twitter api URLs
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorization_url = 'https://api.twitter.com/oauth/authorize'
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    app = Flask(__name__)
    app.config.from_object('src.config.Config') # configを別ファイルのオブジェクトから読み込む
    CORS(app)

    #login_manager = LoginManager()
    #login_manager.init_app(app)
    app.secret_key = b'\x17x\xf0\x83\x93i\x14\xa3\xec<7\x88A\xca\xb5G'

    init_db(app) # databaseの初期化を行う

    @app.route('/')
    def index():
        if 'user_name' in session:
            # セッション変数の取得
            name = session['user_name']
            return f'hello {name}'
        else:
            return redirect(url_for('get_twitter_request_token'))

    @app.route('/show')
    def show_users():
        if 'user_name' in session:
            all_user = User.query.all()
            number_of_user = len(all_user)
            if not number_of_user == 0:
                user_names_list = [user.name for user in all_user]
                strings = '\n'.join(str(user_names_list))
            else:
                strings = ''
            return f'こんにちは{session["user_name"]}. 今ユーザーは{number_of_user}人います. \n' + strings
        else:
            return '''ログインしてください.<a href="/login">ログインページ</a>'''

    '''
    @app.route('/add')
    def add_user():
        #user = User(name='name', email='test@test.com')
        user = User(name='name')
        db.session.add(user)
        db.session.commit()
        return 'ユーザーを増やしました'

    @app.route('/delete')
    def delete_user():
        user = User.query.first()
        if user is not None:
            db.session.delete(user)
            db.session.commit()
            return 'ユーザーを減らしました'
        else:
            return 'ユーザーはひとりもいません'
    '''
    '''
    @app.route('/login', methods=['POST', 'GET'])
    def login_test():
        if request.method == 'POST':
            name = request.form['user_name']
            #email = request.form['email']
            # user情報を確認
            #the_user = User.query.filter(User.email==email).all()
            the_user = User.query.filter(User.name==name).all()
            print(the_user)
            if len(the_user) == 0:
                # 存在しないなら登録処理
                #user = User(name=name, email=email)
                user = User(name=name)
                db.session.add(user)
                db.session.commit()
            else:
                # 存在するならOK（emailはユニークなので）
                name = the_user[0].name

            # セッション変数の設定
            session['user_name'] = name
            return redirect(url_for('index'))
        else:
            return
                    <form method="post">
                        <p><input type=text name=user_name required>
                        <!--<p><input type=text name=email required>-->
                        <p><input type=submit value=login>
                    </form>

    '''

    # 認証画面を返す
    @app.route('/user/login', methods=['GET'])
    def get_twitter_request_token():
        try:
            # リクエストトークンを取得し, 認証urlを取得してリダイレクトする. 失敗したらトップページへのリンクを提示する.
            oauth_callback = "http://127.0.0.1:3000/callback"
            twitter = OAuth1Session(consumer_api_key, consumer_secret_key)
            twitter.fetch_request_token(request_token_url)
            auth_url = twitter.authorization_url(authorization_url)
            return redirect(auth_url)

        except Exception as e:
            print(e)
            #return '''login failed. <a href="http://localhost:3000>top</a>'''
            return f'{e}'

    @app.route('/user/callback', methods=['GET'])
    def callback():
        users_show_url = 'https://api.twitter.com/1.1/users/show.json'
        try:
            # getパラメータを取得
            oauth_token = request.args.get('oauth_token')
            oauth_verifier = request.args.get('oauth_verifier')
            # リクエストトークン取得から返ってきたgetパラメータを用いてアクセストークンを取得. 失敗したら認証のときと同様
            twitter = OAuth1Session(consumer_api_key, consumer_secret_key, oauth_token, oauth_verifier)
            response = twitter.post(access_token_url, params={'oauth_verifier': oauth_verifier})
            access_token = dict(parse_qsl(response.content.decode("utf-8")))

            twitter = OAuth1Session(consumer_api_key, consumer_secret_key, access_token['oauth_token'], access_token['oauth_token_secret'])
            response = twitter.get(users_show_url, params={'user_id': access_token['user_id']})

            if response.status_code == 200:
                user_data = json.loads(response.text)
                users = User.query.filter(User.user_id==access_token['user_id']).all()
                if len(users) == 0:
                    # 存在しないなら登録処理
                    user = User(name=user_data['screen_name'], user_id=access_token['user_id'])
                    db.session.add(user)
                    db.session.commit()

                # セッション変数の設定
                session['session_id'] = str(uuid.uuid4())
                session['user_name'] = access_token['screen_name']
                session['user_id'] = access_token['user_id']
                # session['oauth_token'] = access_token['oauth_token']
                # session['oauth_token_secret'] = access_token['oauth_token_secret']

                # アイコン画像URLから_normalを取り除きオリジナルサイズのものを得ている. https://syncer.jp/Web/API/Twitter/Snippet/4/
                image_url = re.sub(r'_normal', '', user_data['profile_image_url_https'])
                # 返すデータを整えてjsonでreturn
                response_data = {'sessionId': session['session_id'], 'username': session['user_name'], 'profile_image_url': image_url}
                #print(session)
                return jsonify(response_data)
            else:
                raise Exception(f'response status code is not 200 (is {response.status_code})')
        except Exception as e:
            print(e)
            #return '''login failed. <a href="http://localhost:3000>top</a>'''
            return f'{e}'

    @app.route('/user/logout')
    def logout():
        # セッション変数の削除
        session.pop('session_id', None)
        session.pop('user_name', None)
        session.pop('user_id', None)
        session.pop('oauth_token', None)
        session.pop('oauth_secret', None)
        #return redirect(url_for('login_test'))
        return 'logout'

    @app.route('/user/user_delete')
    def logout_and_delete():
        # データベースからユーザー情報を削除
        db.session.query(User).filter(User.id==session['user_id']).delete()
        db.session.commit()
        # セッション変数の削除
        session.pop('session_id', None)
        session.pop('user_name', None)
        session.pop('user_id', None)
        session.pop('oauth_token', None)
        session.pop('oauth_secret', None)
        return 'logout successed and user data deleted'

    return app


app = create_app()