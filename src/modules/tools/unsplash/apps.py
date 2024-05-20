from django.apps import AppConfig


class UnsplashConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.tools.unsplash"
    verbose_name = (
        "Unsplash - Integração com API do Unsplash para busca e uso de imagens."
    )
