from django.db import models


class PagesManager(models.Manager):

    def followers(self, page_id):
        return self.get_queryset().filter(pk=page_id).values_list("followers", flat=True)

    def follow_requests(self, page_id):
        return self.get_queryset().filter(pk=page_id).values_list("follow_requests", flat=True)


class TweetsManager(models.Manager):

    def likes(self, tweet_id):
        return self.get_queryset().filter(pk=tweet_id).values_list("like", flat=True)

