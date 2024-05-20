from django.urls import path

from .views import buscar_imagem

urlpatterns = [
    path("buscar-imagem/", buscar_imagem, name="buscar-imagem"),
]
