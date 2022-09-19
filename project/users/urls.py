from django.urls import path, include

from .routers import router_user

from .views import LoginViewSet, RefreshTokenViewSet

app_name = "user"
urlpatterns = [
    path("token", LoginViewSet.as_view({"post": "login_user"}), name="login"),
    path(
        "token/refresh/",
        RefreshTokenViewSet.as_view({"post": "auth_with_refresh_token"}),
        name="refresh_token",
    ),
    path("", include(router_user.urls)),
]
print(urlpatterns)

