from django.apps import AppConfig


class TweetsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tweets'

    def ready(self):
        from .signals import save_tweet_and_send_email
