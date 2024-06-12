from decimal import Decimal
import hashlib
import hmac
import uuid
import mercadopago
import mercadopago.config
import requests
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
from .models import MercadoPagoDetails, PaymentData
from src.modules.tools.notifications.mail_service import send_email
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

        print(payment)

        reference = uuid.uuid4()

        payment_data = {
            "transaction_amount": payment.transaction_amount,
            "token": payment.token,
            "description": payment.description,
            "payment_method_id": payment.payment_method_id,
            "installments": payment.installments,
            "payer": {"email": payment.payer.email},
            "notification_url": "https://maestri.tech/tools/mp/payment_response/",
            "external_reference": str(reference),
            "statement_descriptor": "Pagamento Matricula Maestri.edu",
            "additional_info": {
                "items": [
                    {
                        "id": "a130356d-78ef-43c1-b9e2-1158f5e76c62",
                        "title": "Curso Maestri.edu",
                        "description": "Matricula inicial para cursos da faculdade Maestri.edu",
                        "category_id": "others",
                        "quantity": 1,
                        "unit_price": 60,
                        "type": "electronics",
                    }
                ]
            },
        }

        if isinstance(payment_data, ListSerializer):
            return Response("d")

        print("code ", payment.promoter_code)

        access_token = secrets.access_token

        promoter = Profile.get_by_promotinal_code(
            promotional_code=payment.promoter_code
        )
        mp_details = MercadoPagoDetails.objects.get(promoter=promoter)
        print(mp_details.access_token)
        access_token = mp_details.access_token
        payment_data["application_fee"] = 15

        print(access_token)

        sdk = mercadopago.SDK(access_token)
        request_options = mercadopago.config.RequestOptions()
        request_options.custom_headers = {"x-idempotency-key": str(uuid.uuid4())}

        result = sdk.payment().create(payment_data, request_options)

        print("\n result: ", result)
        print("\n result[response]", result["response"])

        if isinstance(result["response"]["status"], int):
            if result["response"]["status"] >= 400:
                print("400 error")
                return Response(
                    data={
                        "message": result["response"]["message"],
                    },
                    status=400,
                )

        if result["response"]["status"] == "rejected":
            return Response(
                data={
                    "message": "O pagamento foi rejeitado",
                    "id": result["response"]["id"],
                },
                status=400,
            )

        if result["response"]["status"] == "in_process":
            return Response(
                data={
                    "message": "O pagamento está sendo processado",
                    "id": result["response"]["id"],
                },
                status=400,
            )

        payment_response: PaymentResponseData = PaymentResponseData.create_from_json(
            result["response"]
        )

        print("\n payment-response: ", payment_response, "\n")

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
            origin_id=str(payment_response.id),
            origin_number=str(reference),
        )

        return Response({"id": payment_response.id})


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

        sha = hmac_obj.hexdigest()
        if sha == hash:
            print(manifest)
            print("HMAC verification passed")
        else:
            print(manifest)
            print("HMAC verification failed")
            return Response(status=400)

        if request.data:
            print(request.data)
            return Response(status=200)

        serializer = PaymentUpdateSerializer(data=request.data)

        if isinstance(serializer, ListSerializer):
            print("isList")
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

            user: User = User.objects.get(name=client.profile_id.cpf)

            send_email(
                "Parabéns da Maestri.edu",
                """
                Parabéns por sua grande decisão e por iniciar sua nova grande jornada com a Maestri.edu. 
                Seu pagamento foi aprovado e logo entraremos em contanto com os próximos passos.
                Caso tenha alguma dúvida, por favor entre em contanto por nosso telefone 0800-333-3099.

                Sinceras congratulações da Maestri.edu
                """,
                user.email,
            )

        if payment.action == "payment.create" or payment.action == "payment.created":
            print(payment)
            print("created")

        return Response(status=200)


from rest_framework.permissions import IsAuthenticated


@extend_schema(request=None, responses=None)
class PaymentAuth(APIView):

    permission_classes = (IsAuthenticated,)

    def get(self, request):

        user: User = request.user

        print(user)

        code: str = request.GET.get("code")

        response = requests.post(
            url="https://api.mercadopago.com/oauth/token",
            headers={
                "accept": "application/json",
                "content-type": "application/x-www-form-urlencoded",
            },
            data={
                "client_id": f"{secrets.app_id}",
                "client_secret": f"{secrets.client_secret}",
                "grant_type": "authorization_code",
                "code": f"{code}",
                "redirect_uri": "https://maestri.tech/tools/mp/auth/",
                "state": str(uuid.uuid4()),
            },
        )

        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as errh:
            print("HTTP Error")
            print(errh.args[0])

        if not response.ok or user.profile is None:
            print(response.text)
            return Response(status=response.status_code)

        mp_details = MercadoPagoDetails.create_from_json(
            data=response.json(), promoter=user.profile
        )

        print(mp_details)
        return render(request, "app/main.html")

        return Response(code, status=200)


def payment(request):
    return render(
        request,
        "tools/mercado_pago/payment.html",
        {"public_key": ""},
    )


def register_payment(request):
    print(payment)


# TODO: Ao Receber Webbhook com dinheiro disponível enviar dinheiro via pix para o Inter
