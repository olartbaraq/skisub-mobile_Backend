from .views import SignUpView, LoginView, GetUserView
from django.urls import path


urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign up"),
    path("login/", LoginView.as_view(), name="login"),
    path("get-user/", GetUserView.as_view(), name="get user"),
]
