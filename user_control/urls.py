from .views import SignUpView, LoginView, GetUserView, UpdatePasswordView, DeleteUserView
from django.urls import path



urlpatterns = [
    path("sign-up/", SignUpView.as_view(), name="sign up"),
    path("login/", LoginView.as_view(), name="login"),
    path("get-user/", GetUserView.as_view(), name="get user"),
    path("update-password/", UpdatePasswordView.as_view(), name="update password"),
    path("delete-user/", DeleteUserView.as_view(), name="delete user"),
]
