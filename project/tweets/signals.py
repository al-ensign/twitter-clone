from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from .models import Tweet, Page
from .tasks import send_email_to_followers
import logging
from project.publisher import publisher
import json
from django.contrib.auth import get_user_model
from .services import total_likes_received

User = get_user_model()


@receiver(post_save, sender=Tweet)
def save_tweet_and_send_email(instance, **kwargs):
    logging.info("Received Tweet saved signal")
    tweet = Tweet.objects.get(pk=instance.id)
    followers = Page.pages.followers(tweet.owner_id)
    recipients = []
    logging.info("Collecting users emails")
    for follower in followers:
        user = User.objects.get(pk=follower)
        recipients.append(user.email)
        logging.info("Send celery task")
        send_email_to_followers.delay(body=tweet.text, recipients=recipients)

    # Send data to rabbitmq to update stats in microservice
    data = {
        "user_id": tweet.owner.owner.id,
        "page_id": tweet.owner_id,
        "tweets": tweet.owner.tweets.count(),
        "likes": total_likes_received(tweet.owner),
    }
    logging.info("Sending message to publisher")
    publisher.publish(json.dumps(data))


post_save.connect(save_tweet_and_send_email, sender=Tweet)


@receiver(post_delete, sender=Tweet)
def tweet_deleted(instance, **kwargs):
    tweet = Tweet.objects.get(pk=instance.id)
    data = {
        "user_id": tweet.owner.owner.id,
        "page_id": tweet.owner_id,
        "tweets": tweet.owner.tweets.count(),
        "likes": total_likes_received(tweet.owner),
    }
    publisher.publish(json.dumps(data))


post_delete.connect(tweet_deleted, sender=Tweet)


@receiver(post_save, sender=Page)
def save_page_stats(instance, **kwargs):
    logging.info("Received Page saved signal")
    page = Page.objects.get(pk=instance.id)

    # Send data to rabbitmq to update stats in microservice
    data = {
        "user_id": page.owner_id,
        "page_id": instance.id,
        "followers": Page.pages.followers(instance.id).exclude(followers=None).count(),
        "follow_requests": Page.pages.follow_requests(instance.id).exclude(follow_requests=None).count(),
        "tweets": page.tweets.count(),
        "likes": total_likes_received(page),
        "is_blocked": page.is_blocked,
        "status": "Exists",
    }

    logging.info("Sending message to publisher")
    publisher.publish(json.dumps(data))


post_save.connect(save_page_stats, sender=Page)


@receiver(pre_delete, sender=Page)
def page_deleted(instance, **kwargs):
    page = Page.objects.get(pk=instance.id)
    data = {
        "page_id": instance.id,
        "user_id": page.owner_id,
        "status": "Deleted",
    }
    publisher.publish(json.dumps(data))


pre_delete.connect(page_deleted, sender=Page)
