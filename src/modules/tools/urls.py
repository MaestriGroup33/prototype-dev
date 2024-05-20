from django.urls import include
from django.urls import path

urlpatterns = [
    path("", include("src.modules.tools.unsplash.urls")),
    path("", include("src.modules.tools.aipag.urls")),
    path("mp/", include("src.modules.tools.mercado_pago.urls")),
]
