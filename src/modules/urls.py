from django.urls import include
from django.urls import path

urlpatterns = [
    path("core/", include("src.modules.core.urls")),
    path("edu/", include("src.modules.edu.urls")),
    path("tools/", include("src.modules.tools.urls")),
]
