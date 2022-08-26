from .views import UserViewSet, LoginViewSet, RefreshTokenViewSet
from rest_framework import routers

router_user = routers.DefaultRouter()
router_user.register(r"users", UserViewSet)
