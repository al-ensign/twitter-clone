from django.urls import path, include
from tweets.routers import (
    router_comment,
    router_tweet,
    router_tag,
    router_page,
)

app_name = "tweets"
urlpatterns = [
    path("", include(router_page.urls)),
    path("", include(router_tweet.urls)),
    path("", include(router_comment.urls)),
    path("", include(router_tag.urls)),
]


