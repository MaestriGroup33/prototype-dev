from django.apps import AppConfig


class CampaignsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.edu.campaigns"
    verbose_name = (
        "Campanhas - Gerenciamento de campanhas de marketing e vendas da Maestri.edu"
    )
