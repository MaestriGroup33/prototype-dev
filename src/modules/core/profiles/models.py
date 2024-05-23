import uuid
from datetime import date
from datetime import datetime

from django.db import models

from .choices import GENDER_CHOICES
from .choices import GRADUATION_TYPE_CHOICES
from .choices import MARITAL_STATUS_CHOICES
from .choices import POSTGRADUATION_TYPE_CHOICES
from .choices import SITUATION_EDUCATION_CHOICES
from .choices import STATE_CHOICES
from .choices import STATUS_ACADEMIC_CHOICES
from .validators import validate_birthdate


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=100,
        help_text=("Nome completo."),
        verbose_name=("Nome"),
    )
    birth_date = models.DateField(
        validators=[validate_birthdate],
        help_text=("Data de Nascimento"),
        verbose_name=("Data de Nascimento"),
    )
    cpf = models.CharField(
        max_length=14,
        unique=True,
        help_text=('CPF no formato "somente números".'),
        verbose_name=("CPF - Cadastro de Pessoa Física"),
    )
    phone = models.CharField(
        max_length=11,
        help_text=("Número de celular com Whatsapp"),
        verbose_name=("Telefone"),
    )
    gender = models.CharField(
        max_length=1,
        choices=GENDER_CHOICES,
        help_text=("Gênero"),
        verbose_name=("Gênero (Sexo)"),
    )
    marital_status = models.CharField(
        max_length=1,
        choices=MARITAL_STATUS_CHOICES,
        help_text=("Estado civil"),
        verbose_name=("Estado Civil"),
    )
    academic_status = models.CharField(
        max_length=1,
        choices=STATUS_ACADEMIC_CHOICES,
        help_text=("Escolaridade"),
        verbose_name=("Escolaridade"),
    )
    mother_name = models.CharField(
        max_length=100,
        help_text=("Nome completo da mãe."),
        verbose_name=("Nome da Mãe"),
    )
    birth_state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        help_text=("Estado de nascimento."),
        verbose_name=("Estado de Nascimento"),
    )
    birth_city = models.CharField(
        max_length=100,
        help_text=("Cidade de nascimento."),
        verbose_name=("Cidade de Nascimento"),
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=("Criado em"))
    address_bool = models.BooleanField(
        default=False,
        verbose_name=("Endereço Cadastrado"),
        help_text=("Endereço cadastrado."),
        editable=False,
    )
    educational_bool = models.BooleanField(
        default=False,
        verbose_name=("Escolaridade Cadastrada"),
        help_text=("Escolaridade cadastrada."),
        editable=False,
    )
    profile_bool = models.BooleanField(
        default=False,
        verbose_name=("Perfil Cadastrado"),
        help_text=("Perfil cadastrado."),
        editable=False,
    )
    age = models.PositiveIntegerField(verbose_name=("Idade"))

    class Meta:
        verbose_name_plural = "Perfis"
        unique_together = [["cpf", "birth_date"]]  # Exemplo de uso de unique_together

    def __str__(self):
        return "name"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    # pylint: disable=too-many-arguments
    @staticmethod
    def create(
        name: str,
        birth_date: date,
        cpf: str,
        phone: str,
        gender: str,
        marital_status: str,
        academic_status: str,
        mother_name: str,
        birth_state: str,
        birth_city: str,
        age: int,
    ):
        return Profile.objects.create(
            id=uuid.uuid4(),
            name=name,
            birth_date=birth_date,
            cpf=cpf,
            phone=phone,
            gender=gender,
            marital_status=marital_status,
            academic_status=academic_status,
            mother_name=mother_name,
            birth_state=birth_state,
            birth_city=birth_city,
            created_at=datetime.now().date(),
            address_bool=False,
            educational_bool=False,
            profile_bool=False,
            age=age,
        )


class Location(models.Model):
    """Modelo base para compartilhar localização comum entre diferentes modelos."""

    city = models.CharField(
        max_length=255,
        verbose_name="Cidade",
        help_text="Escolha a cidade.",
    )
    state = models.CharField(
        max_length=2,
        choices=STATE_CHOICES,
        verbose_name="Estado",
        help_text="Escolha o estado.",
    )

    class Meta:
        abstract = True

    @staticmethod
    def create(
        city: str,
        state: str,
    ):
        return Location.objects.create(
            city=city,
            state=state,
        )


class Address(Location):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Perfil",
    )
    cep = models.CharField(max_length=9, verbose_name="CEP", help_text="Código Postal.")
    street = models.CharField(max_length=255, verbose_name="Rua")
    number = models.CharField(max_length=10, verbose_name="Número")
    complement = models.CharField(
        max_length=255,
        verbose_name="Complemento",
        blank=True,
        null=True,
    )
    neighborhood = models.CharField(max_length=255, verbose_name="Bairro")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Endereço"
        verbose_name_plural = "Endereços"

    def __str__(self):
        return f"{self.street}, {self.number} - {self.cep}"

    @staticmethod
    def create(
        profile_id: uuid.UUID,
        cep: str,
        street: str,
        number: str,
        complement: str,
        neighborhood: str,
    ):
        return Address.objects.create(
            profile=profile_id,
            cep=cep,
            street=street,
            number=number,
            complement=complement,
            neighborhood=neighborhood,
            created_at=datetime.now().date(),
        )


class HighSchool(Location):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Perfil",
        related_name="high_school",
        related_query_name="high_school",
    )
    institution_name = models.CharField(
        max_length=255,
        verbose_name="Nome da Instituição",
    )
    situation = models.CharField(
        max_length=33,
        choices=SITUATION_EDUCATION_CHOICES,
        verbose_name="Situação",
        help_text="Atual situação do ensino médio.",
    )
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(verbose_name="Data de Conclusão", null=True, blank=True)
    certificate = models.FileField(
        upload_to="certificates/",
        verbose_name="Certificado",
        help_text="Certificado de conclusão do ensino médio.",
    )
    history = models.FileField(
        upload_to="histories/",
        verbose_name="Histórico",
        help_text="Histórico escolar do ensino médio.",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Ensino Médio"
        verbose_name_plural = "Informações sobre Ensino Médio"

    def __str__(self):
        return f"{self.institution_name} - {self.city}, {self.state}"


class EducationalProgram(Location):
    """Modelo base para programas educacionais que compartilham campos comuns."""

    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Perfil",
        related_name="educational_programs",
        related_query_name="educational_program",
    )
    institution_name = models.CharField(
        max_length=255,
        verbose_name="Nome da Instituição",
        help_text="Nome da instituição de ensino.",
    )
    situation = models.CharField(
        max_length=1,
        choices=SITUATION_EDUCATION_CHOICES,
        verbose_name="Situação",
        help_text="Situação atual do curso.",
    )
    start_date = models.DateField(verbose_name="Data de Início")
    end_date = models.DateField(verbose_name="Data de Conclusão", null=True, blank=True)
    course_name = models.CharField(max_length=255, verbose_name="Nome do Curso")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Atualizado em")

    class Meta:
        abstract = True


class Graduation(EducationalProgram):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Perfil",
        related_name="graduation",
        related_query_name="graduation",
    )
    graduation_type = models.CharField(
        max_length=1,
        choices=GRADUATION_TYPE_CHOICES,
        verbose_name="Tipo de Graduação",
        help_text="Tipo de graduação.",
    )
    certificate = models.FileField(
        upload_to="certificates/",
        verbose_name="Diploma",
        help_text="Diploma de conclusão da graduação.",
    )
    history = models.FileField(
        upload_to="histories/",
        verbose_name="Histórico",
        help_text="Histórico e Ementa da graduação cursada.",
    )
    duration = models.CharField(
        max_length=255,
        verbose_name="Duração",
        help_text="Tempo de duração do curso.",
    )

    class Meta:
        verbose_name = "Informação sobre a graduação"
        verbose_name_plural = "Informações sobre as graduações"

    def __str__(self):
        return f"{self.course_name} - {self.institution_name}"


class PostGraduation(EducationalProgram):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        verbose_name="Perfil",
        related_name="postgraduation",
        related_query_name="postgraduation",
    )
    postgraduation_type = models.CharField(
        max_length=1,
        choices=POSTGRADUATION_TYPE_CHOICES,
        verbose_name="Tipo de Pós-Graduação",
        help_text="Tipo de pós-graduação.",
    )
    certificate = models.FileField(
        upload_to="certificates/",
        verbose_name="Diploma",
        help_text="Diploma de conclusão da pós-graduação.",
    )
    curriculum = models.FileField(
        upload_to="curriculums/",
        verbose_name="Ementa",
        help_text="Ementa da pós-graduação cursada.",
    )
    duration = models.CharField(
        max_length=255,
        verbose_name="Duração",
        help_text="Tempo de duração do curso.",
    )

    class Meta:
        verbose_name = "Informação sobre a pós-graduação"
        verbose_name_plural = "Informações sobre as pós-graduações"

    def __str__(self):
        return f"{self.course_name} - {self.institution_name}"


class Documents(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)
    contract_user_promoter = models.FileField(
        upload_to="contracts/",
        verbose_name="Contrato do Promotor",
        help_text="Contrato do promotor.",
        editable=False,
    )
    contract_user_promoter_sign_bool = models.BooleanField(
        default=False,
        verbose_name="Contrato Assinado",
        help_text="Contrato assinado.",
        editable=False,
    )
    contract_user_agreement = models.FileField(
        upload_to="contracts/",
        verbose_name="Contrato do Convênio",
        help_text="Contrato do convênio.",
        editable=False,
    )
    contract_user_agreement_sign_bool = models.BooleanField(
        default=False,
        verbose_name="Contrato Assinado",
        help_text="Contrato assinado.",
        editable=False,
    )
    promoter_contract_signing_photo = models.ImageField(
        upload_to="photos/",
        verbose_name="Foto/Assinatura do contrato de promotor",
        help_text="Foto/Assinatura do contrato.",
        editable=False,
    )
    agreement_contract_signing_photo = models.ImageField(
        upload_to="photos/",
        verbose_name="Foto/Assinatura do contrrato de convênio",
        help_text="Foto/Assinatura do contrato.",
        editable=False,
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        abstract = True

    def __str__(self):
        return "self.profile.name"


class ContractsEnrollment(Documents):
    contract_client_enrollment = models.FileField(
        upload_to="contracts/",
        verbose_name="Contrato da Matrícula",
        help_text="Contrato de matrícula.",
        editable=False,
    )
    enrollment_contract_signing_photo = models.ImageField(
        upload_to="photos/",
        verbose_name="Foto/Assinatura do Contrato de Matrícula.",
        help_text="Foto/Assinatura do contrato de matrícula.",
        editable=False,
    )
    enrollment_contract_sign_bool = models.BooleanField(
        default=False,
        verbose_name="Contrato Assinado",
        help_text="Contrato assinado.",
        editable=False,
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Criado em")

    class Meta:
        verbose_name = "Contrato de Matrícula"
        verbose_name_plural = "Contratos de Matrícula"

    def __str__(self):
        return "self.profile.name"
