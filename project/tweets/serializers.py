from rest_framework import serializers
from .models import Page, Tag, Tweet, Comment
from django.contrib.auth import get_user_model

User = get_user_model()


class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Page
        fields = (
            "id",
            "title",
            "uuid",
            "description",
            "tags",
            "owner",
            "followers",
            "path",
            "is_private",
            "follow_requests",
            "is_blocked",
            "unblock_date",
        )
        extra_kwargs = {
            "followers": {
                "required": False,
                "allow_null": True
            },
            "follow_requests": {
                "required": False,
                "allow_null": True
            },
            "tags": {
                "required": False,
                "allow_null": True
            }
        }


class OnePageSerializer(serializers.ModelSerializer):
    page_id = serializers.IntegerField()

    class Meta:
        model = Page
        fields = ("page_id",)


class TempBlockPageSerializer(serializers.ModelSerializer):
    page_id = serializers.IntegerField()
    unblock_date = serializers.DateTimeField(input_formats=["%d/%m/%Y"])

    class Meta:
        model = Page
        fields = (
            "page_id",
            "unblock_date",
        )


class AcceptRejectFollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField()

    class Meta:
        model = Page
        fields = ("user_id",)


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = (
            "id",
            "owner",
            "text",
            "created_at",
            "updated_at",
            "like",
        )

        extra_kwargs = {
            "like": {
                "required": False,
                "allow_null": True
            },
        }


class OneTweetSerializer(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()

    class Meta:
        model = Tweet
        fields = ("tweet_id",)


class LikeUnlikeTweetSerializer(serializers.ModelSerializer):
    tweet_id = serializers.IntegerField()
    page_id = serializers.IntegerField()

    class Meta:
        model = Tweet
        fields = ("tweet_id", "page_id",)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "owner",
            "tweet",
            "text",
            "created_at",
            "updated_at",
        )


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ("id", "name",)

