from django.urls import path

from .views import CampaignEnrollment

app_name = "modules.edu.enrollment"
urlpatterns = [
    path(
        "initial-campaign/",
        view=CampaignEnrollment.as_view(),
    ),
]
