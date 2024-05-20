from django.apps import AppConfig


class FinancesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.core.finances"
    verbose_name = (
        "Finanças - Gerenciamento de comissões, contas e fluxos "
        "de caixa da Maestri.group"
    )
