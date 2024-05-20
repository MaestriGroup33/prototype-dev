from rest_framework import serializers

from .models import GlobalSettings
from .models import Indicators


class GlobalSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalSettings
        fields = ["id", "year_base"]


class IndicatorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Indicators
        fields = [
            "id",
            "year_base",
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
