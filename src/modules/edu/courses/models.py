from datetime import datetime

from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _


class DurationChoices(models.TextChoices):
    TWO_SEMESTERS = "12", _("2 Semestres")
    THREE_SEMESTERS = "18", _("3 Semestres")
    FOUR_SEMESTERS = "24", _("4 Semestres")
    FIVE_SEMESTERS = "30", _("5 Semestres")
    SIX_SEMESTERS = "36", _("6 Semestres")
    SEVEN_SEMESTERS = "42", _("7 Semestres")
    EIGHT_SEMESTERS = "48", _("8 Semestres")
    NINE_SEMESTERS = "54", _("9 Semestres")
    TEN_SEMESTERS = "60", _("10 Semestres")


class TypeChoices(models.TextChoices):
    TECHNOLOGIST = "tec", _("Tecnólogo")
    LICENTIATE_R2 = "r2", _("Licenciatura R2")
    BACHELOR = "bch", _("Bacharelado")
    LICENTIATE = "lic", _("Licenciatura")
    PEDAGOGIC = "pg", _("Formação Pedagógica")


class AreaChoices(models.TextChoices):
    ADMINISTRATION = "adm", _("Administração")
    JURIDICAL_SCIENCES = "cj", _("Ciências Jurídicas")
    PERSONAL_DEVELOPMENT = "dp", _("Desenvolvimento Pessoal")
    EDUCATION = "edu", _("Educação")
    EAD_EDUCATION = "ead", _("Educação EAD")
    ENGINEERING_AND_ARCHITECTURE = "ea", _("Engenharia e Arquitetura")
    HOTOGRAPHY_AND_VIDEO = "fv", _("Fotografia e Vídeo")
    MANAGEMENT_AND_BUSINESS = "gn", _("Gestão e Negócios")
    PROFESSIONAL_INDICATION = "ip", _("Indicação Profissional")
    MARKETING_AND_COMMUNICATION = "mc", _("Marketing e Comunicação")
    HUMAN_RESOURCES = "rh", _("Recursos Humanos")
    HEALTH_AND_WELLNESS = "sb", _("Saúde e Bem-estar")
    TECHNOLOGY = "tec", _("Tecnologia")
    INFORMATION_TECHNOLOGY = "ti", _("Tecnologia da Informação")
    PEDAGOGIC = "pg", _("Formação Pedagógica")


class Course(models.Model):
    cod = models.CharField(
        max_length=255,
        verbose_name=_("Código"),
        help_text=_(
            "Código do Curso, exemplo: adm-administração, mpr-Ministério Pastoral...",
        ),
    )
    name = models.CharField(
        max_length=255,
        verbose_name=_("Nome"),
        help_text=_("Nome do curso"),
    )
    description = models.TextField(
        verbose_name=_("Descrição"),
        help_text=_("Descrição do curso"),
    )
    duration = models.CharField(
        max_length=2,
        choices=DurationChoices.choices,
        verbose_name=_("Duração"),
        help_text=_("Duração do curso"),
    )
    type = models.CharField(
        max_length=3,
        choices=TypeChoices.choices,
        verbose_name=_("Tipo"),
        help_text=_("Tipo do curso"),
    )
    area = models.CharField(
        max_length=3,
        choices=AreaChoices.choices,
        verbose_name=_("Área"),
        help_text=_("Área do curso"),
    )
    information = models.TextField(
        verbose_name=_("Informações"),
        help_text=_("Informações do curso"),
    )
    objective = models.TextField(
        verbose_name=_("Objetivo"),
        help_text=_("Objetivo do curso"),
    )
    jobmarket = models.TextField(
        verbose_name=_("Mercado de Trabalho"),
        help_text=_("Mercado de Trabalho"),
    )
    specifics = models.TextField(
        verbose_name=_("Informações Específicas"),
        help_text=_("Informações Específicas"),
    )
    curriculum = models.TextField(
        verbose_name=_("Grade Curricular"),
        help_text=_("Grade Curricular"),
    )
    avatar = models.ImageField(
        upload_to="courses",
        verbose_name=_("Avatar"),
        help_text=_("Avatar do curso"),
    )

    class Meta:
        verbose_name = _("Curso")
        verbose_name_plural = _("Cursos")
        ordering = ("name",)

        def __str__(self):
            return self.name

    @staticmethod
    def create(
        cod: str,
        name: str,
        description: str,
        duration: str,
        type: str,
        area,
        str,
        information: str,
        objective: str,
        jobmarket: str,
        specifics: str,
        curriculum: str,
        avatar: models.FileField,
    ):
        return Course.objects.create(
            cod=cod,
            name=name,
            description=description,
            duration=duration,
            type=type,
            area=area,
            information=information,
            objective=objective,
            jobmarket=jobmarket,
            specifics=specifics,
            curriculum=curriculum,
            avatar=avatar,
        )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("edu:courses:detail", kwargs={"slug": self.slug})

    def avatar_img(self):
        return (
            f'<img src="{self.avatar.url}" width="50"'
            ' height="50" style="border-radius: 50%;">',
        )

    avatar_img.short_description = _("Avatar")


class CourseReview(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="reviews")
    name = models.CharField(max_length=255, verbose_name=_("Nome"))
    email = models.EmailField(verbose_name=_("E-mail"))
    review = models.TextField(verbose_name=_("Avaliação"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Criado em"))

    class Meta:
        verbose_name = _("Avaliação")
        verbose_name_plural = _("Avaliações")
        ordering = ("-created_at",)

    def __str__(self):
        return self.name

    @staticmethod
    def create(
        course: int,
        name: str,
        email: str,
        review: str,
    ):
        return CourseReview.objects.create(
            course=course,
            name=name,
            email=email,
            review=review,
            created_at=datetime.now().date(),
        )
