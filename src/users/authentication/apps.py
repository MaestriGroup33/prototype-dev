from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersAuthenticationConfig(AppConfig):
    name = "src.users.authentication"
    verbose_name = _("Auth")
