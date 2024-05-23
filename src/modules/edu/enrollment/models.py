import datetime
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from src.modules.core.profiles.models import Profile
from src.modules.edu.campaigns.models import LandingPage
from src.modules.edu.courses.models import Course
from src.modules.edu.courses.utils import calculate_payment_duration


class ClassificationPrices:
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    classification = models.CharField(max_length=2)
    commission = models.IntegerField()


class Classifications(models.Model):
    classification = models.CharField(max_length=2)
    commission = models.IntegerField()

    @staticmethod
    def create(
        classification: str,
        commission: int,
    ) -> "Classifications":
        return Classifications.objects.create(
            classification=classification,
            commission=commission,
        )

    def save(self, *args, **kwargs):
        # Import local para evitar importação circular
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Classificação"
        verbose_name_plural = "Classificações"

    def __str__(self):
        return f"{self.classification}"


class ClientStatus(models.TextChoices):
    LEAD = "LEAD", _("Lead")
    PRE_ENROLLED = "PRE_ENROLLED", _("Aluno Pré-Matriculado")
    ENROLLED = "ENROLLED", _("Aluno Matriculado")
    RE_ENROLLED = "RE_ENROLLED", _("Veterano")
    CANCELLED = "CANCELLED", _("Cancelado")
    SUSPENDED = "SUSPENDED", _("Trancado")
    TRANSFERRED = "TRANSFERRED", _("Transferido")
    ALUMNI = "ALUMNI", _("Ex-Aluno")
    BLOCKED = "BLOCKED", _("Aluno com Pendências Financeiras")
    OTHER = "OTHER", _("Outro")


class Clients(models.Model):
    profile_id = models.ForeignKey(Profile, on_delete=models.CASCADE)
    promoter_id = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        help_text="Tutor responsável pelo aluno.",
        verbose_name="Tutor Responsável",
        related_name="tutor_responsible",
        blank=False,
        null=False,
    )  # Promotor responsável aluno
    status = models.CharField(
        max_length=16,
        choices=ClientStatus.choices,
        help_text="Status do cliente.",
        verbose_name="Status do Cliente",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    classification = models.ForeignKey(
        Classifications,
        on_delete=models.CASCADE,
    )
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.profile_id.name

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"

    @staticmethod
    def create(
        profile: Profile,
        promoter_id: uuid.UUID,
        status: ClientStatus,
        classification: Classifications,
    ):

        promoter = Profile.objects.get(id=promoter_id)

        return Clients.objects.create(
            profile_id=profile,
            promoter_id=promoter,
            status=status,
            classification=classification,
            created_at=datetime.datetime.now(),
            updated_at=datetime.datetime.now(),
        )


# TODO: ADD ENROLLMENT FEE FIELD
class Enrollments(models.Model):
    student = models.ForeignKey(Clients, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    campaign = models.ForeignKey(LandingPage, on_delete=models.CASCADE)
    duration_months = models.IntegerField()
    monthly_value = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_payment_counter = models.IntegerField()
    payed_enrollment_fee = models.BooleanField()

    @staticmethod
    def create(
        student: Clients,
        course_code: str | None,
        campaign_id: int | None,
    ):
        if course_code is None:
            course_code = 1

        if campaign_id is None:
            campaign_id = 1

        course: Course = Course.objects.get(id=course_code)
        campaign: LandingPage = LandingPage.objects.get(id=campaign_id)

        return Enrollments.objects.create(
            student=student,
            course=course,
            campaign=campaign,
            duration_months=calculate_payment_duration(
                int(course.duration),
                student.classification.classification,
            ),
            monthly_payment_counter=0,
            monthly_value=0,
            payed_enrollment_fee=False,
        )
