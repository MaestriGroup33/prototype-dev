import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from .managers import UserManager


class UserGroups(models.TextChoices):
    Promoter = "PR", _("Promotor")
    Covenant = "CV", _("Convenio")
    Student = "ST", _("Aluno")


class User(AbstractUser):
    """
    Default custom user model for Maestri.group.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    name = CharField(_("Nome do usuario"), blank=True, max_length=255)
    first_name = None
    last_name = None
    email = EmailField(
        _("endereço de email"),
        unique=True,
    )
    username = None
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})

    @staticmethod
    def create(
        name: str,
        email: str,
        password: str,
        group: UserGroups | None,
        covenant_id: uuid.UUID,
    ) -> "User":
        if group is None:
            group = UserGroups.Promoter

        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            group=group,
            covenant_id=covenant_id,
        )

        # from .groups import add_user_to_group

        # add_user_to_group(user)

        return user
