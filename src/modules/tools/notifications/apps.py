from django.apps import AppConfig


class ToolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.tools.notifications"
    verbose_name = "Serviços de Notificações. Email, Messagens, etc."
