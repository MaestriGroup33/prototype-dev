from django.urls import path

from . import views

app_name = "src.modules.app"
urlpatterns = [
    path(
        "edit-promo-code2",
        view=views.edit_promo,
    ),
    path("finance/", view=views.finances, name="finance"),
]
