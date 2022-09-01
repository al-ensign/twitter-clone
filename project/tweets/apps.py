from django.apps import AppConfig
from django.db.models.signals import post_save


class TweetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweets'

    def ready(self):
        # Implicitly connect signal handlers decorated with @receiver.
        from .signals import save_tweet_and_send_email
        # Explicitly connect a signal handler.
        # post_save.connect(save_tweet_and_send_email)

