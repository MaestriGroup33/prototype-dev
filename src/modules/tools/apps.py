from django.apps import AppConfig


class ToolsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.tools"
    verbose_name = (
        "Ferramentas - Gerenciamento de ferramentas, configurações e apis externas."
    )
