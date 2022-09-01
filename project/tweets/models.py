from django.db import models
import uuid
from django.conf import settings
from .managers import PagesManager, TweetsManager


class Tag(models.Model):
    name = models.CharField(max_length=30, unique=True)


class Page(models.Model):
    title = models.CharField(max_length=80)
    uuid = models.UUIDField(default=uuid.uuid4, unique=True, max_length=32)
    description = models.TextField()
    tags = models.ManyToManyField(Tag, related_name="pages")
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="pages"
    )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="followers"
    )
    path = models.URLField(null=True, blank=True)
    is_private = models.BooleanField(default=False)
    follow_requests = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="requests"
    )
    is_blocked = models.BooleanField(default=False)
    unblock_date = models.DateTimeField(null=True, blank=True)

    objects = models.Manager()
    pages = PagesManager()


class Tweet(models.Model):
    owner = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="tweets"
    )
    text = models.CharField(max_length=280, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date updated")
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="likes")

    objects = models.Manager()
    tweets = TweetsManager()


class Comment(models.Model):
    owner = models.ForeignKey(
        Page, on_delete=models.CASCADE, related_name="comments"
    )
    tweet = models.ForeignKey(Tweet, on_delete=models.CASCADE, related_name="comments")
    text = models.CharField(max_length=280, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Date created")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Date updated")
