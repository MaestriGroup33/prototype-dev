# Create your models here.
from datetime import date
from datetime import datetime
from datetime import timedelta
from decimal import Decimal

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.modules.edu.enrollment.models import Enrollments


class ChargeStatus(models.TextChoices):
    AWAITING_CONFIRMATION = "WL", _("Aguardando Liberação")
    AWAITING_PAYMENT = "WP", _("Aguardando pagamento")
    PAYED = "P", _("Pago")
    ANALYSIS = "AN", _("Análise")
    BLOCKED = "BK", _("Bloqueado")
    CANCELED = "CN", _("Cancelado")


class ChargeOrigin(models.TextChoices):
    MP = "MP", _("Mercado Pago")
    INTER = "INT", _("Inter Bank")


class Charge(models.Model):
    enrollment_id = models.ForeignKey(
        Enrollments,
        on_delete=models.CASCADE,
        null=False,
    )
    value = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    created_date = models.DateField()
    status = models.CharField(
        verbose_name="Status",
        max_length=2,
        choices=ChargeStatus.choices,
        default="WP",
    )
    origin = models.CharField(
        verbose_name="Origin", max_length=3, choices=ChargeOrigin.choices, default="MP"
    )
    origin_id = models.CharField(verbose_name="Origin Code")
    origin_number = models.CharField(verbose_name="Origin Number")
    bar_code = models.CharField(verbose_name="Bar Code", null=True, blank=True)
    pix_code = models.CharField(verbose_name="Pix Code", null=True, blank=True)
    simple_pix_code = models.CharField(
        verbose_name="Simple Pix Code", null=True, blank=True
    )
    txid = models.CharField(verbose_name="Txid", null=True, blank=True)

    @staticmethod
    def create(
        enrollment_id: Enrollments,
        value: Decimal,
        status: ChargeStatus,
        days_until_due: int = 30,
    ):
        due_date = date.today() + timedelta(days_until_due)
        return Charge.objects.create(
            enrollment_id=enrollment_id,
            value=value,
            due_date=due_date,
            created_date=datetime.now().date(),
            status=status,
        )
