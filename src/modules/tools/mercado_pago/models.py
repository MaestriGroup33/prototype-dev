from dataclasses import dataclass
from django.db import models

from src.modules.core.profiles.models import Profile


@dataclass
class PaymentUser:
    cpf: str
    email: str
    cellphone: str
    course_code: str
    campaign_id: int


@dataclass
class PaymentData:
    transaction_amount: str
    token: str
    description: str
    payment_method_id: str
    installments: int
    payer: PaymentUser
    cpf: str
    promoter_code: str | None


class PaymentUpdate(models.Model):
    action = models.CharField(max_length=50)
    api_version = models.CharField(max_length=10)
    request_id = models.CharField(max_length=50)
    date_created = models.DateTimeField()
    payment_id = models.CharField(max_length=50)
    live_mode = models.BooleanField()
    type = models.CharField(max_length=50)
    user_id = models.BigIntegerField()

    def _str_(self):
        return f"PaymentUpdate {self.payment_id}"


class MercadoPagoDetails(models.Model):
    access_token = models.CharField(
        max_length=300,
        help_text="Token de Acesso.",
        verbose_name="Token de Acesso",
    )
    public_key = models.CharField(
        max_length=300,
        help_text="Chave mp",
        verbose_name="Chave mp",
    )
    refresh_token = models.CharField(
        max_length=300,
        verbose_name="Refresh_token",
    )
    user_id = models.CharField(
        max_length=300,
        help_text="MP user_id",
    )
    promoter = models.ForeignKey(Profile, on_delete=models.CASCADE)

    @staticmethod
    def create(
        access_token: str,
        public_key: str,
        refresh_token: str,
        user_id: str,
        promoter: Profile,
    ):
        return MercadoPagoDetails.objects.create(
            access_token=access_token,
            public_key=public_key,
            refresh_token=refresh_token,
            user_id=user_id,
            promoter=promoter,
        )

    @staticmethod
    def create_from_json(data: dict, promoter: Profile):
        return MercadoPagoDetails.create(
            access_token=data["access_token"],
            public_key=data["public_key"],
            refresh_token=data["refresh_token"],
            user_id=data["user_id"],
            promoter=promoter,
        )
