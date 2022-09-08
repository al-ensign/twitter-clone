import os
import jwt
import logging


logger = logging.getLogger(__name__)


def decode_token_and_get_user(request):
    authorization_header = request.headers.get("Authorization")
    if not authorization_header:
        return None

    prefix, token = authorization_header.split(" ")

    if prefix != os.getenv('TOKEN_TYPE'):
        return None

    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET_KEY"), algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise logger.error("Access_token expired"),
    except IndexError:
        raise logger.error("Token prefix missing")

    user_id = payload["sub"]

    return user_id
