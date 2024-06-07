from django.urls import path
from .views import login_view, register

app_name = "src.users.authentication"
urlpatterns = [
    path("login/", view=login_view, name="login_view"),
    path("register/", view=register, name="register"),
]
