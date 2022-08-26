from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class LoginUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "username",
            "password",
        )


class RefreshTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id",)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "name",
            "password",
            "email",
            "image_s3_path",
            "role",
            "is_blocked",
        )


class OneUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = ("id",)


class BlockUserSerializer(serializers.ModelSerializer):
    user_to_block = OneUserSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "user_to_block",
        )


class UnblockUserSerializer(serializers.ModelSerializer):
    blocked_user = OneUserSerializer(many=True)

    class Meta:
        model = User
        fields = (
            "id",
            "blocked_user",
        )
