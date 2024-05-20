from django import forms

from .models import GlobalSettings
from .models import Indicators


class GlobalSettingsForm(forms.ModelForm):
    class Meta:
        model = GlobalSettings
        fields = ["year_base"]  # Inclui apenas o campo year_base para o formulário
        labels = {"year_base": "Ano Base"}
        help_texts = {"year_base": "Informe o ano base para os cálculos."}


class IndicatorsForm(forms.ModelForm):
    class Meta:
        model = Indicators
        fields = [
            "salario_minimo",
            "ipca",
            "inpc",
            "igpm",
            "selic",
            "poupanca",
            "cdi",
            "dolar",
            "euro",
            "bitcoin",
            "bolsa",
        ]
        labels = {
            "salario_minimo": "Salário Mínimo",
            "ipca": "IPCA",
            "inpc": "INPC",
            "igpm": "IGPM",
            "selic": "SELIC",
            "poupanca": "Poupança",
            "cdi": "CDI",
            "dolar": "Dólar",
            "euro": "Euro",
            "bitcoin": "Bitcoin",
            "bolsa": "Bolsa de Valores",
        }
        help_texts = {
            "salario_minimo": "Defina o salário mínimo atual.",
            "ipca": "Defina o IPCA acumulado no ano.",
            "inpc": "Defina o INPC acumulado no ano.",
            "igpm": "Defina o IGPM acumulado no ano.",
            "selic": "Defina a SELIC acumulada no ano.",
            "poupanca": "Defina o rendimento da poupança acumulado no ano.",
            "cdi": "Defina o CDI acumulado no ano.",
            "dolar": "Defina a cotação atual do dólar.",
            "euro": "Defina a cotação atual do euro.",
            "bitcoin": "Defina a cotação atual do bitcoin.",
            "bolsa": "Defina o valor atual do índice da bolsa de valores.",
        }
