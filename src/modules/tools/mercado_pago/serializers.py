from rest_framework import serializers
from .models import PaymentUpdate, PaymentData, PaymentUser


class PaymentUserSerializer(serializers.Serializer):
    cpf = serializers.CharField()
    email = serializers.EmailField()


class PaymentDataSerializer(serializers.Serializer):
    transaction_amount = serializers.CharField()
    token = serializers.CharField()
    description = serializers.CharField()
    payment_method_id = serializers.CharField()
    installments = serializers.IntegerField()
    payer = PaymentUserSerializer()
    campaign_id = serializers.CharField()
    cpf = serializers.CharField()
    cellphone = serializers.CharField()
    course_code = serializers.CharField()

    @staticmethod
    def create_from_json(json_data: dict) -> PaymentData:
        return PaymentData(
            transaction_amount=json_data["transaction_amount"],
            token=json_data["token"],
            description=json_data["description"],
            payment_method_id=json_data["payment_method_id"],
            installments=json_data["installments"],
            payer=PaymentUser(
                cpf=json_data["payer"]["cpf"],
                email=json_data["payer"]["email"],
                cellphone=json_data["cellphone"],
                course_code=json_data.get("course_code", "1"),
                campaign_id=json_data.get("campaign_id", "1"),
            ),
            cpf=json_data["cpf"],
        )


class PaymentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentUpdate
        fields = "__all__"

    @staticmethod
    def create_from_json(json_data):
        return PaymentUpdate(
            action=json_data["action"],
            api_version=json_data["api_version"],
            request_id=json_data["id"],
            date_created=json_data["date_created"],
            payment_id=json_data["data"]["id"],
            live_mode=json_data["live_mode"],
            type=json_data["type"],
            user_id=json_data["user_id"],
        )
