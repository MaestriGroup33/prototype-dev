from decimal import Decimal

from django import forms
from django.db import models

from src.modules.core.profiles.models import Profile
from src.modules.edu.charges.models import Charge

TYPE_CHOICES = [
    ("T", "Taxa de Matrícula"),
    ("M", "Mensalidade"),
]

STATUS_CHOICES = [
    ("P", "Pago"),
    ("A", "Aguardando Pagamento"),
    ("C", "Cancelado"),
]


class Account(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    charge_id = models.ForeignKey(Charge, on_delete=models.CASCADE)
    transaction_type = models.CharField(
        max_length=1,
        choices=TYPE_CHOICES,
        db_column="type",
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Conta"
        verbose_name_plural = "Contas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.profile_id}"

    @staticmethod
    def create(profile_id, balance, charge_id, transaction_type, status):
        return Account.objects.create(
            profile_id=profile_id,
            balance=balance,
            charge_id=charge_id,
            transaction_type=transaction_type,
            status=status,
        )


class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ["profile_id", "balance", "charge_id", "transaction_type", "status"]


class GlobalSettings(models.Model):
    year_base = models.IntegerField(
        verbose_name="Ano Base",
        help_text="Ano base para cálculos de mensalidades.",
    )

    class Meta:
        verbose_name = "Configuração Global"
        verbose_name_plural = "Configurações Globais"

    def __str__(self):
        return f"Configurações Globais - {self.year_base}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    @staticmethod
    def create(year_base):
        return GlobalSettings.objects.create(year_base=year_base)


class Indicators(GlobalSettings):
    salario_minimo = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Salário Mínimo",
        default=Decimal("1412.00"),
        help_text="Salário mínimo atual.",
    )
    ipca = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="IPCA",
        default=Decimal("0.03"),
        help_text="IPCA acumulado no ano.",
    )
    inpc = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="INPC",
        default=Decimal("0.03"),
        help_text="INPC acumulado no ano.",
    )
    igpm = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="IGPM",
        default=Decimal("0.03"),
        help_text="IGPM acumulado no ano.",
    )
    selic = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="SELIC",
        default=Decimal("0.03"),
        help_text="SELIC acumulado no ano.",
    )
    poupanca = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Poupança",
        default=Decimal("0.03"),
        help_text="Rendimento da poupança acumulado no ano.",
    )
    cdi = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="CDI",
        default=Decimal("0.03"),
        help_text="CDI acumulado no ano.",
    )
    dolar = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Dólar",
        default=Decimal("5.00"),
        help_text="Cotação do dólar no ano.",
    )
    euro = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Euro",
        default=Decimal("6.00"),
        help_text="Cotação do euro no ano.",
    )
    bitcoin = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Bitcoin",
        default=Decimal("50000.00"),
        help_text="Cotação do bitcoin no ano.",
    )
    bolsa = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Bolsa de Valores",
        default=Decimal("100000.00"),
        help_text="Valor do índice da bolsa de valores no ano.",
    )

    class Meta:
        verbose_name = "Indicador"
        verbose_name_plural = "Indicadores"

    def __str__(self):
        return f"Indicadores - Ano Base {self.year_base}"

    @staticmethod
    def get_minimum_wage():
        min_wage = Indicators.objects.last()
        if min_wage is None:
            return Decimal("1412.00")
        return min_wage.salario_minimo
