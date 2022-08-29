import jwt
from rest_framework import exceptions
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


def save_path(user_id, file_name):
    user = User.objects.get(pk=user_id)
    user.image_s3_path = file_name
    return user.save()


def block_user(admin_id, user_to_block_id):

    """
    Block user: Set User.is_blocked = True
    """

    admin = User.objects.get(pk=admin_id)
    user_to_block = User.objects.get(pk=user_to_block_id)
    if admin.Roles.ADMIN:
        user_to_block.is_blocked = True
        return user_to_block.save()


def unblock_user(admin_id, blocked_user):

    """
    Unblock user: Set User.is_blocked = True
    """

    admin = User.objects.get(pk=admin_id)
    blocked_user = User.objects.get(pk=blocked_user)
    if admin.Roles.ADMIN:
        blocked_user.is_blocked = False
        return blocked_user.save()


def verify_user_login(username, password):

    """
    Verify credentials to Login User
    """

    if not username or not password:
        raise exceptions.AuthenticationFailed('Username and Password are required')

    user = User.objects.filter(username=username).first()

    if not user:
        raise exceptions.AuthenticationFailed('User not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('Wrong password')

    return user


def verify_refresh_token(refresh_token):

    """
    Verify and decode Refresh token to get a valid User
    """

    if not refresh_token:
        raise exceptions.AuthenticationFailed(
            "Authentication credentials were not provided."
        )
    try:
        payload = jwt.decode(
            refresh_token, settings.JWT_SECRET_KEY, algorithms=["HS256"]
        )
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            "Expired refresh token, please login again."
        )

    user = User.objects.filter(id=payload.get("sub")).first()
    if not user:
        raise exceptions.AuthenticationFailed("User not found")

    if not user.is_active:
        raise exceptions.AuthenticationFailed("User is inactive")

    if user.is_blocked:
        raise exceptions.AuthenticationFailed("User is blocked")

    return user
