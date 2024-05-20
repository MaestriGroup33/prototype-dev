from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("src.modules.core.profiles.urls")),
    # path("finances/", include("modules.core.finances.urls")),
]
# TODO: urls.finances foi comentado
