from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (AuthorListView, ProfileView, RegisterAPIView,
                         RegisterView, sms_verification)

app_name = UsersConfig.name

# Что с апи делать?
urlpatterns = [
    # API URLs
    path("api/register/", RegisterAPIView.as_view(), name="api-register"),
    path(
        "api/login/",
        TokenObtainPairView.as_view(permission_classes=(AllowAny,)),
        name="api-login",
    ),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="api-token-refresh"),
    # Web URLs
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("sms-confirm/", sms_verification, name="sms-confirm"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("authors/", AuthorListView.as_view(), name="authors"),
]
