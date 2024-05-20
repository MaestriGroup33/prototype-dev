from django.urls import path

from .views import maestri_group_site

urlpatterns = [
    path("group", maestri_group_site, name="Site Oficial da Maestri.group"),
]
