import uuid
from dataclasses import dataclass

from rest_framework import serializers

from .models import Classifications


@dataclass
class CampaignEnrollmentModel:
    cpf: str
    phone: str
    promoter_id: uuid.UUID | None
    course_code: str | None
    campaign_id: int | None


class CampaignEnrollmentSerializer(serializers.Serializer):
    cpf = serializers.CharField(max_length=11)
    phone = serializers.CharField(max_length=11)
    promoter_id = serializers.UUIDField()
    course_code = serializers.CharField()
    campaign_id = serializers.IntegerField()

    def create(self, validated_data) -> CampaignEnrollmentModel:
        return CampaignEnrollmentModel(
            cpf=validated_data.get("cpf"),
            phone=validated_data.get("phone"),
            promoter_id=validated_data.get("promoter_id", None),
            course_code=validated_data.get("course_code", None),
            campaign_id=validated_data.get("campaign_id", None),
        )


class CommentSerializer(serializers.Serializer):
    email = serializers.EmailField()
    content = serializers.CharField(max_length=200)
    created = serializers.DateTimeField()

    def create(self, validated_data):
        return CampaignEnrollmentModel(**validated_data)


class ClassificationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classifications
        fields = ["id", "course_id", "base_price", "classification", "price"]
        read_only_fields = ["price"]  # O campo price é calculado automaticamente

    def create(self, validated_data):
        instance = Classifications(**validated_data)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        instance.base_price = validated_data.get("base_price", instance.base_price)
        instance.classification = validated_data.get(
            "classification",
            instance.classification,
        )
        # Recalcula o preço, se necessário
        instance.save()
        return instance
