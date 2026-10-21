from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView

app_name = "users"

urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="users/login.html",
        extra_context={"show_signup": True},
    ), name="login"),

    path("logout/", LogoutView.as_view(), name="logout")
]