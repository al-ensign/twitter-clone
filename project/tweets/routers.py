from .views import PageViewSet, TweetViewSet, CommentViewSet, TagViewSet
from rest_framework import routers

router_page = routers.DefaultRouter()
router_page.register(r"pages", PageViewSet)

router_tweet = routers.DefaultRouter()
router_tweet.register(r"tweets", TweetViewSet)

router_comment = routers.DefaultRouter()
router_comment.register(r"comments", CommentViewSet)

router_tag = routers.DefaultRouter()
router_tag.register(r"tags", TagViewSet)
