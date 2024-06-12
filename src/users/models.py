import uuid
from typing import ClassVar

from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


from src.modules.core.profiles.models import Profile

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
    user_group = CharField(
        verbose_name="user group",
        choices=UserGroups.choices,
        max_length=2,
        default="ST",
    )
    profile = models.ForeignKey(
        Profile, verbose_name=_("Profile"), on_delete=models.CASCADE, null=True
    )
    covenant_id = models.ForeignKey(
        Profile,
        null=True,
        related_name="created_by_%(class)s_related",
        on_delete=models.SET_NULL,
    )
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username, profile"]

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
        covenant_id: Profile | None,
    ) -> "User":
        """Creates and Saves a user to the database. Returns the created user"""
        if group is None:
            group = UserGroups.Promoter

        user = User.objects.create_user(
            email=email,
            password=password,
            name=name,
            user_group=group,
            covenant_id=covenant_id,
        )

        # group = Group.objects.get(name=user.groups.name)
        # group.user_set.add(user)

        return user
