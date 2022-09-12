import datetime
import jwt
from django.conf import settings
from django.contrib.auth import get_user_model


User = get_user_model()


def generate_token(exp, user: User) -> str:  # noqa
    """
    Generates JWT token.
    """
    token_payload = {
        "sub": user.id,
        "exp": exp,
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(token_payload, settings.JWT_SECRET_KEY, algorithm="HS256")
    return token
