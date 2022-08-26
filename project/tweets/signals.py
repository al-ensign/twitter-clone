from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tweet, Page
from .tasks import send_email_to_followers
import logging
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Tweet)
def save_tweet_and_send_email(sender, instance, **kwargs):

    logging.info("Received Tweet saved signal")

    tweet = Tweet.objects.get(pk=instance.id)
    page_id = tweet.owner_id

    page_queryset = Page.objects.filter(pk=page_id)
    body = tweet.text
    list_of_followers = page_queryset.values_list("followers", flat=True)
    recipients = []

    logging.info("Collecting users emails")

    for follower in list_of_followers:
        user = User.objects.get(pk=follower)
        email = user.email
        recipients.append(email)

    logging.info("Send celery task")

    send_email_to_followers.delay(body=body, recipients=recipients)

    logging.info("Send celery task")


