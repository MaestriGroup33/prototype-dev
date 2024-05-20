from rest_framework import serializers

from .models import Card
from .models import Faq
from .models import LandingPage
from .models import Section
from .models import Statistic
from .models import Testimonial
from .models import ValueProposition


class CardSerializer(serializers.ModelSerializer):
    """Serializer para o modelo Card, incluindo detalhes
    como seção associada e texto do cartão."""

    class Meta:
        model = Card
        fields = ["id", "section", "icon", "title", "text"]


class StatisticSerializer(serializers.ModelSerializer):
    """Serializer para estatísticas
    associadas a seções específicas."""

    class Meta:
        model = Statistic
        fields = ["id", "section", "title", "value", "icon"]


class TestimonialSerializer(serializers.ModelSerializer):
    """Serializer para depoimentos, vinculados
    a uma página de destino específica."""

    class Meta:
        model = Testimonial
        fields = [
            "id",
            "landing_page_id",
            "text",
            "author_name",
            "author_title",
            "author_photo",
        ]


class ValuePropositionSerializer(serializers.ModelSerializer):
    """Serializer para propostas de valor,
    que detalham elementos como valor e frequência."""

    class Meta:
        model = ValueProposition
        fields = [
            "id",
            "landing_page_id",
            "icon",
            "title",
            "text",
            "value",
            "frequency",
        ]


class SectionSerializer(serializers.ModelSerializer):
    cards = CardSerializer(many=True, read_only=True)
    statistics = StatisticSerializer(many=True, read_only=True)
    """Serializer para seções de uma página de
    destino, incluindo cartões e estatísticas associados."""

    class Meta:
        model = Section
        fields = [
            "id",
            "landing_page_id",
            "title",
            "subtitle",
            "text",
            "image",
            "cards",
            "statistics",
            "additional_info",
        ]


class FaqSerializer(serializers.ModelSerializer):
    """Serializer para perguntas frequentes,
    vinculadas a uma página de destino específica."""

    class Meta:
        model = Faq
        fields = ["id", "question", "answer", "landing_page_id"]
        """Serializer para perguntas frequentes,
        vinculadas a uma página de destino específica."""


class LandingPageSerializer(serializers.ModelSerializer):
    sections = SectionSerializer(many=True, read_only=True)
    testimonials = TestimonialSerializer(many=True, read_only=True)
    value_propositions = ValuePropositionSerializer(many=True, read_only=True)
    faqs = FaqSerializer(many=True, read_only=True)
    """Serializer para páginas de destino, agregando
    seções, depoimentos e propostas de valor."""

    class Meta:
        model = LandingPage
        fields = [
            "id",
            "name",
            "campaign_start",
            "campaign_end",
            "active",
            "sections",
            "testimonials",
            "value_propositions",
            "faqs",
        ]
