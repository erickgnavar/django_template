from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "users"

urlpatterns = [
    path("signup", views.SignupView.as_view(), name="signup"),
    path(
        "login",
        auth_views.LoginView.as_view(template_name="users/login.html"),
        name="login",
    ),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "confirm-email/<slug:token>",
        views.ConfirmEmailView.as_view(),
        name="confirm-email",
    ),
    path("forgot-password", views.ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "reset-password/<slug:token>",
        views.ResetPasswordView.as_view(),
        name="reset-password",
    ),
    path(
        "change-password",
        auth_views.PasswordChangeView.as_view(
            template_name="users/change-password.html", success_url="/"
        ),
        name="change-password",
    ),
]
