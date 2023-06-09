import os
import jwt
import os
import sys
from fastapi import Request


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def decode_token_and_get_user(request: Request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return None

    prefix, token = authorization_header.split(" ")

    if prefix != os.getenv('TOKEN_TYPE'):
        return None

    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise ValueError("Access_token expired")
    except IndexError:
        raise BaseException("Token prefix missing")

    user_id = payload["sub"]

    return user_id
