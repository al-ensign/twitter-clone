from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Tweet, Page
from .tasks import send_email_to_followers
import logging
from django.contrib.auth import get_user_model

User = get_user_model()


@receiver(post_save, sender=Tweet)
def save_tweet_and_send_email(instance, created, **kwargs):

    logging.info("Received Tweet saved signal")
    if created:
        tweet = Tweet.objects.get(pk=instance.id)
        followers = Page.pages.followers(tweet.owner_id)
        recipients = []
        logging.info("Collecting users emails")
        for follower in followers:
            user = User.objects.get(pk=follower)
            recipients.append(user.email)
            logging.info("Send celery task")
            send_email_to_followers.delay(body=tweet.text, recipients=recipients)


post_save.connect(save_tweet_and_send_email, sender=Tweet)
