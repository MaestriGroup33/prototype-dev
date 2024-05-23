from decimal import Decimal

from django.db import models
from django.db.models import JSONField

from src.modules.edu.courses.models import Course


class BaseSection(models.Model):
    title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Título",
        help_text="Título da seção. Opcional.",
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Subtítulo",
        help_text="Subtítulo da seção. Opcional.",
    )
    text = models.TextField(
        blank=True,
        verbose_name="Texto",
        help_text="Texto principal da seção. Opcional.",
    )
    image = models.FileField(
        upload_to="images/",
        blank=True,
        null=True,
        verbose_name="Imagem",
        help_text="Imagem da seção. Suporta PNG/SVG. Opcional.",
    )
    additional_info = JSONField(
        default=dict,
        blank=True,
        verbose_name="Informações Adicionais",
        help_text="Campo JSON para dados adicionais. Flexível e opcional.",
    )

    class Meta:
        abstract = True
        verbose_name = "Seção Base"
        verbose_name_plural = "Seções Base"

    def __str__(self):
        return self.title


class LandingPage(models.Model):
    name = models.CharField(
        max_length=200,
        verbose_name="Nome",
        help_text="Nome da página de destino.",
    )
    campaign_start = models.DateField(
        verbose_name="Início da Campanha",
        help_text="Data de início da campanha.",
    )
    campaign_end = models.DateField(
        verbose_name="Fim da Campanha",
        help_text="Data de término da campanha.",
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Indica se a campanha está ativa.",
    )

    class Meta:
        verbose_name = "Página de Destino"
        verbose_name_plural = "Páginas de Destino"

    def __str__(self):
        return self.name


class Section(BaseSection):
    landing_page_id = models.ForeignKey(
        LandingPage,
        related_name="sections",
        on_delete=models.CASCADE,
        verbose_name="Página de Destino",
        help_text="Página de destino à qual a seção pertence.",
    )

    class Meta:
        verbose_name = "Seção"
        verbose_name_plural = "Seções"

    def __str__(self):
        return self.title


class Card(models.Model):
    section = models.ForeignKey(
        Section,
        related_name="cards",
        on_delete=models.CASCADE,
        verbose_name="Seção",
        help_text="Seção à qual o cartão pertence.",
    )
    icon = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ícone",
        help_text="URL ou caminho para o ícone SVG. Opcional.",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título do cartão.",
    )
    text = models.TextField(
        verbose_name="Texto",
        help_text="Texto principal do cartão.",
    )

    class Meta:
        verbose_name = "Cartão"
        verbose_name_plural = "Cartões"

    def __str__(self):
        return self.title


class Statistic(models.Model):
    section = models.ForeignKey(
        Section,
        related_name="statistics",
        on_delete=models.CASCADE,
        verbose_name="Seção",
        help_text="Seção à qual a estatística pertence.",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título da estatística.",
    )
    value = models.CharField(
        max_length=200,
        verbose_name="Valor",
        help_text="Valor da estatística.",
    )
    icon = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ícone",
        help_text="URL ou caminho para o ícone SVG. Opcional.",
    )

    class Meta:
        verbose_name = "Estatística"
        verbose_name_plural = "Estatísticas"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    landing_page_id = models.ForeignKey(
        LandingPage,
        related_name="testimonials",
        on_delete=models.CASCADE,
        verbose_name="Página de Destino",
        help_text="Página de destino à qual o depoimento pertence.",
    )
    text = models.TextField(verbose_name="Texto", help_text="Texto do depoimento.")
    author_name = models.CharField(
        max_length=200,
        verbose_name="Nome do Autor",
        help_text="Nome do autor do depoimento.",
    )
    author_title = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Título do Autor",
        help_text="Título profissional do autor do depoimento. Opcional.",
    )
    author_photo = models.ImageField(
        upload_to="testimonials/",
        blank=True,
        null=True,
        verbose_name="Foto do Autor",
        help_text="Foto do autor do depoimento. Opcional.",
    )

    class Meta:
        verbose_name = "Depoimento"
        verbose_name_plural = "Depoimentos"

    def __str__(self):
        return self.author_name


class ValueProposition(models.Model):
    landing_page_id = models.ForeignKey(
        LandingPage,
        related_name="value_propositions",
        on_delete=models.CASCADE,
        verbose_name="Página de Destino",
        help_text="Página de destino à qual a proposta de valor pertence.",
    )
    icon = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Ícone",
        help_text="Ícone relacionado à proposta de valor. Opcional.",
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título da proposta de valor.",
    )
    text = models.TextField(
        verbose_name="Texto",
        help_text="Descrição da proposta de valor.",
    )
    value = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Valor",
        help_text="Valor numérico da proposta.",
    )
    frequency = models.CharField(
        max_length=50,
        verbose_name="Frequência",
        help_text="Frequência de aplicação do valor, como 'Mensal', 'Anual', 'Única'.",
    )

    class Meta:
        verbose_name = "Proposta de Valor"
        verbose_name_plural = "Propostas de Valor"

    def __str__(self):
        return f"{self.title} - {self.value}"


class Faq(models.Model):
    question = models.TextField(verbose_name="Pergunta")
    answer = models.TextField(verbose_name="Resposta")
    landing_page_id = models.ForeignKey(
        LandingPage,
        on_delete=models.CASCADE,
        related_name="faqs",
        verbose_name="Página de Destino",
        help_text="Deixe em branco para perguntas gerais, ou escolha uma "
        "página de destino específica para perguntas específicas.",
    )

    class Meta:
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question

    # class GlobalSettings(models.Model):
    #     year_base = models.IntegerField(
    #         verbose_name="Ano Base",
    #         help_text="Ano base para cálculos de mensalidades.",
    #     )

    # class Indicators(GlobalSettings):
    #     salario_minimo = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="Salário Mínimo",
    #         default=Decimal(1412.00),
    #         help_text="Salário mínimo atual.",
    #     )
    #     ipca = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="IPCA",
    #         default=Decimal(0.03),
    #         help_text="IPCA acumulado no ano.",
    #     )
    #     inpc = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="INPC",
    #         default=Decimal(0.03),
    #         help_text="INPC acumulado no ano.",
    #     )
    #     igpm = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="IGPM",
    #         default=Decimal(0.03),
    #         help_text="IGPM acumulado no ano.",
    #     )
    #     selic = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="SELIC",
    #         default=Decimal(0.03),
    #         help_text="SELIC acumulado no ano.",
    #     )
    #     poupanca = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="Poupança",
    #         default=Decimal(0.03),
    #         help_text="Rendimento da poupança acumulado no ano.",
    #     )
    #     cdi = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="CDI",
    #         default=Decimal(0.03),
    #         help_text="CDI acumulado no ano.",
    #     )
    #     dolar = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="Dólar",
    #         default=Decimal(5.00),
    #         help_text="Cotação do dólar no ano.",
    #     )
    #     euro = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="Euro",
    #         default=Decimal(6.00),
    #         help_text="Cotação do euro no ano.",
    #     )
    #     bitcoin = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="Bitcoin",
    #         default=Decimal(50000.00),
    #         help_text="Cotação do bitcoin no ano.",
    #     )
    #     bolsa = models.DecimalField(
    #         max_digits=10,
    #         decimal_places=2,
    #         verbose_name="Bolsa de Valores",
    #         default=Decimal(100000.00),
    #         help_text="Valor do índice da bolsa de valores no ano.",
    #     )

    #     class Meta:
    #         verbose_name = "Configuração Global"
    #         verbose_name_plural = "Configurações Globais"

    #     def __str__(self):
    #         return f"Configurações Globais - {self.year_base}"

    #     def save(self, *args, **kwargs):
    #         super().save(*args, **kwargs)

    #     # class Classifications(models.Model):
    #     course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    #     base_price = models.DecimalField(max_digits=10, decimal_places=2)
    #     classification = models.CharField(max_length=1)
    #     price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    #     def save(self, *args, **kwargs):
    #         from .utilities import calculate_tuition

    #         # Obtém o último valor de salário mínimo inserido
    #         salario_minimo = Classifications.get_min_salary()
    #         self.price = calculate_tuition(
    #             self.classification,
    #             self.base_price,
    #             salario_minimo,
    #         )

    #         super().save(*args, **kwargs)

    #     class Meta:
    #         verbose_name = "Classificação"
    #         verbose_name_plural = "Classificações"

    #     def __str__(self):
    #         return f"{self.course_id} - {self.classification} - {self.price}"

    # @staticmethod
    # def get_min_salary():
    #     min = Indicators.objects.last()

    #     if min is None:
    #         return 1412.00

    #     return min.salario_minimo
