from django.db import router
from django.urls import path

from . import views

router.register(
    r"globalsettings",
    views.GlobalSettingsViewSet,
    basename="globalsettings",
)
router.register(r"indicators", views.IndicatorsViewSet, basename="indicators")


urlpatterns = [
    path("details", view=views.GlobalSettingsFormView.as_view()),
    path(
        "global-settings/",
        views.GlobalSettingsFormView.as_view(),
        name="globalsettings_form",
    ),
    path(
        "global-settings-func/",
        views.global_settings_form,
        name="globalsettings_form_func",
    ),
    path("indicators/", views.IndicatorsFormView.as_view(), name="indicators_form"),
    path("indicators-func/", views.indicators_form, name="indicators_form_func"),
]
