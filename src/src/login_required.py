import functools
from typing import Union
from flask import request
from werkzeug.exceptions import Unauthorized
from werkzeug.datastructures import WWWAuthenticate
from src.models import User


class NotAuthorized(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def get_session_id() -> str:
    session_id = request.json.get("sessionID", "")
    if not session_id:
        raise NotAuthorized("not authorized")
    return session_id


def login_required(method):
    # デコレータとして定義. これをつけたメソッドにアクセスするには認証が必要になる.
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            session_id = get_session_id()
            user: Union[User, None] = User.query.filter(
                User.session_id == session_id
            ).first()
            if user is None:
                raise NotAuthorized("user not found.")
        except NotAuthorized as e:
            print(e)
            raise Unauthorized(
                description="session is not valid",
                www_authenticate=WWWAuthenticate(
                    "Bearer", {"error": "invalid session"}
                ),
            )
        return method(*args, **kwargs, user=user)

    return wrapper
