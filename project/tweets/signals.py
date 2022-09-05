from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tweet, Page
from .tasks import send_email_to_followers
import logging
from project.publisher import publisher
import json
from django.contrib.auth import get_user_model

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
        "tweet_id": instance.id,
        "owner_id": tweet.owner_id,
        "likes": len(Tweet.tweets.likes(instance.id)),
    }
    logging.info("Sending message to publisher")
    publisher.publish(json.dumps(data))


post_save.connect(save_tweet_and_send_email, sender=Tweet)


@receiver(post_save, sender=Page)
def save_page_stats(instance, **kwargs):
    logging.info("Received Page saved signal")
    page = Page.objects.get(pk=instance.id)

    # Send data to rabbitmq to update stats in microservice
    data = {
        "page_id": instance.id,
        "owner_id": page.owner_id,
        "followers": len(Page.pages.followers(instance.id)),
        "follow_requests": len(Page.pages.follow_requests(instance.id)),
        "is_blocked": page.is_blocked,
    }

    logging.info("Sending message to publisher")
    publisher.publish(json.dumps(data))


post_save.connect(save_page_stats, sender=Page)
