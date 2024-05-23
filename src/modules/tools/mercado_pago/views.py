from decimal import Decimal
import hashlib
import hmac
import uuid
import mercadopago
import mercadopago.config
from django.shortcuts import render
from src.modules.edu.charges.models import Charge, ChargeStatus
from src.modules.tools.mercado_pago.models import PaymentUpdate
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.serializers import ListSerializer
from src.modules.tools.mercado_pago.response import PaymentResponseData
from . import secrets
from .secrets import secret_key
from .serializers import PaymentDataSerializer, PaymentUpdateSerializer
from .models import PaymentData
from src.modules.core.profiles.models import Profile
from src.modules.edu.enrollment.models import ClientStatus, Enrollments, Clients
from src.users.models import User, UserGroups
from django.utils.crypto import get_random_string


class Payment(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        request=PaymentDataSerializer,
        responses={201: PaymentDataSerializer},
    )
    def post(self, request):
        """
        Creates a new payment
        """

        payment: PaymentData = PaymentDataSerializer.create_from_json(request.data)

        payment_data = {
            "transaction_amount": payment.transaction_amount,
            "token": payment.token,
            "description": payment.description,
            "payment_method_id": payment.payment_method_id,
            "installments": payment.installments,
            "payer": {"email": payment.payer.email},
        }

        if isinstance(payment_data, ListSerializer):
            return Response("d")

        print(payment_data)

        sdk = mercadopago.SDK(secrets.access_token)
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {"x-idempotency-key": str(uuid.uuid4())}

        result = sdk.payment().create(payment_data, request_options)

        print(result["response"])

        if result["response"]["status"] == 400:
            return Response(result["response"]["message"], 400)

        payment_response: PaymentResponseData = PaymentResponseData.create_from_json(
            result["response"]
        )

        print("\n payment: ", payment_response, "\n")

        payment: PaymentData = PaymentDataSerializer.create_from_json(request.data)

        print("payment ", payment)

        profile: Profile = Profile.objects.get(cpf=payment.cpf)

        client: Clients = Clients.objects.get(profile_id=profile)

        user: User = User.create(
            name=payment.cpf,
            email=payment.payer.email,
            password=get_random_string(length=32),
            group=UserGroups.Student,
            covenant_id=None,
        )

        enrollment: Enrollments = Enrollments.create(
            student=client,
            course_code=payment.payer.course_code,
            campaign_id=payment.payer.campaign_id,
        )

        enrollment.save()

        charge: Charge = Charge.create(
            enrollment_id=enrollment,
            value=Decimal(payment.transaction_amount),
            status=ChargeStatus.AWAITING_PAYMENT,
        )

        return Response(request.data)


@extend_schema(request=None, responses=None)
class PaymentResponse(APIView):
    authentication_classes = []  # disables authentication
    permission_classes = []  # disables permission

    def post(self, request):
        x_signature = request.headers.get("x-signature")
        x_request_id = request.headers.get("x-request-id")

        data_id = request.GET.get("data.id", "d")

        # Separating the x-signature into parts
        parts = x_signature.split(",")

        # Initializing variables to store ts and hash
        ts = None
        hash = None

        # Iterate over the values to obtain ts and v1
        for part in parts:
            # Split each part into key and value
            key_value = part.split("=", 1)
            if len(key_value) == 2:
                key = key_value[0].strip()
                value = key_value[1].strip()
                if key == "ts":
                    ts = value
                elif key == "v1":
                    hash = value

        # Obtain the secret key for the user/application from Mercadopago developers site
        secret = secret_key

        # Generate the manifest string
        manifest = f"id:{data_id};request-id:{x_request_id};ts:{ts};"

        # Create an HMAC signature defining the hash type and the key as a byte array
        hmac_obj = hmac.new(
            secret.encode(),
            msg=manifest.encode(),
            digestmod=hashlib.sha256,
        )

        # Obtain the hash result as a hexadecimal string
        sha = hmac_obj.hexdigest()
        if sha == hash:
            # HMAC verification passed
            print("HMAC verification passed")
        else:
            # HMAC verification failed
            print("HMAC verification failed")
            return Response(status=400)

        serializer = PaymentUpdateSerializer(data=request.data)

        if isinstance(serializer, ListSerializer):
            return Response(status=400)

        payment: PaymentUpdate = serializer.create_from_json(
            json_data=serializer.initial_data
        )

        if payment.action == "payment.update" or payment.action == "payment.updated":
            charge: Charge = Charge.objects.get(origin_id=payment.payment_id)
            charge.status = ChargeStatus.PAYED
            charge.save()
            enrollment: Enrollments = charge.enrollment_id
            enrollment.payed_enrollment_fee = True
            enrollment.save()
            client: Clients = enrollment.student
            client.status = ClientStatus.PRE_ENROLLED
            client.save()

        if payment.action == "payment.create":
            print("create")

        return Response(status=200)


def payment(request):
    return render(
        request,
        "tools/mercado_pago/payment.html",
        {"public_key": ""},
    )


def register_payment(request):
    print(payment)


# TODO: Ao Receber Webbhook com dinheiro disponível enviar dinheiro via pix para o Inter
