from dataclasses import dataclass
from django.db import models


@dataclass
class PaymentUser:
    cpf: str
    email: str
    cellphone: str
    course_code: str


@dataclass
class PaymentData(models.Model):
    transaction_amount: str
    token: str
    description: str
    payment_method_id: str
    installments: int
    payer: PaymentUser
    campaign_id: int


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
