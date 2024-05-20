# urls.py
from django.urls import path

from .views import get_cidades

urlpatterns = [
    path("cidades/", get_cidades, name="get_cidades"),
    # outras urls...
]
