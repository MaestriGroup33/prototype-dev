# Create your views here.
import datetime

from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.serializers import ListSerializer
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError
from src.modules.core.profiles.models import Profile

from .forms import ClassificationsForm
from .models import Classifications
from .models import Clients
from .models import ClientStatus
from .models import Enrollments
from .serializers import CampaignEnrollmentSerializer
from .serializers import ClassificationsSerializer


class CampaignEnrollment(APIView):
    authentication_classes = [TokenAuthentication]

    @extend_schema(
        request=CampaignEnrollmentSerializer,
        responses={201: CampaignEnrollmentSerializer},
    )
    def post(self, request):
        """
        Create a new Enrollment
        """

        print(request.data)
        # return Response(status=200, data=request.data)

        campaign_enrollment = CampaignEnrollmentSerializer(data=request.data)

        if isinstance(campaign_enrollment, ListSerializer):
            return Response(data=campaign_enrollment.data, status=403)

        pre_enrollment = campaign_enrollment.create(campaign_enrollment.initial_data)

        print("cpf, promoterId: ", pre_enrollment.cpf, pre_enrollment.promoter_id)

        if Profile.objects.filter(cpf=pre_enrollment.cpf).exists():
            raise ParseError("CPF já cadastrado")

        profile: Profile = Profile.create(
            name=pre_enrollment.cpf,
            birth_date=datetime.datetime.now().date(),
            cpf=pre_enrollment.cpf,
            phone=pre_enrollment.phone,
            gender="",
            marital_status="",
            academic_status="",
            mother_name="",
            birth_state="",
            birth_city="",
            age=18,
        )

        print("Profile: ", profile)

        client: Clients = Clients.create(
            profile=profile,
            promoter_id=pre_enrollment.promoter_id,
            status=ClientStatus.LEAD,
            classification=Classifications.objects.get(classification="X"),
        )

        enrollment: Enrollments = Enrollments.create(
            student=client,
            course_code=pre_enrollment.course_code,
            campaign_id=pre_enrollment.campaign_id,
        )

        return Response(data=campaign_enrollment.initial_data)


class ClassificationsViewSet(viewsets.ModelViewSet):
    queryset = Classifications.objects.all()
    serializer_class = ClassificationsSerializer
    permission_classes = [permissions.IsAuthenticated]


class ClassificationsFormView(FormView):
    template_name = "classifications_form.html"
    form_class = ClassificationsForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Classificação salva com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


def classifications_form(request):
    if request.method == "POST":
        form = ClassificationsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Classificação salva com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = ClassificationsForm()

    return render(request, "classifications_form.html", {"form": form})
