from django import forms

from .models import Card
from .models import Faq
from .models import LandingPage
from .models import Section
from .models import Statistic
from .models import Testimonial
from .models import ValueProposition


class LandingPageForm(forms.ModelForm):
    class Meta:
        model = LandingPage
        fields = ["name", "campaign_start", "campaign_end", "active"]
        widgets = {
            "campaign_start": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
            ),
            "campaign_end": forms.DateInput(
                attrs={"type": "date", "class": "form-control"},
            ),
        }
        help_texts = {
            "name": "Insira o nome da página de destino.",
            "campaign_start": "Selecione a data de início da campanha.",
            "campaign_end": "Selecione a data de término da campanha.",
            "active": "Marque se a campanha está ativa.",
        }


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = [
            "landing_page_id",
            "title",
            "subtitle",
            "text",
            "image",
            "additional_info",
        ]
        widgets = {
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "subtitle": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.FileInput(attrs={"class": "form-control"}),
            "additional_info": forms.Textarea(
                attrs={"class": "form-control"},
            ),
        }
        help_texts = {
            "landing_page_id": "Selecione a página de destino associada.",
            "title": "Insira o título da seção, se houver.",
            "subtitle": "Insira o subtítulo da seção, se houver.",
            "text": "Digite o texto principal da seção.",
            "image": "Carregue uma imagem para a seção.",
            "additional_info": "Adicione informações adicionais no formato JSON.",
        }


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["section", "icon", "title", "text"]
        widgets = {
            "section": forms.Select(attrs={"class": "form-control"}),
            "icon": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(
                attrs={"class": "form-control", "rows": 3},
            ),
        }
        help_texts = {
            "section": "Selecione a seção à qual o cartão pertence.",
            "icon": "Insira a URL ou caminho para o ícone SVG.",
            "title": "Digite o título do cartão.",
            "text": "Digite o texto principal do cartão.",
        }


class StatisticForm(forms.ModelForm):
    class Meta:
        model = Statistic
        fields = ["section", "title", "value", "icon"]
        widgets = {
            "section": forms.Select(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "value": forms.TextInput(attrs={"class": "form-control"}),
            "icon": forms.TextInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "section": "Selecione a seção à qual a estatística pertence.",
            "title": "Digite o título da estatística.",
            "value": "Digite o valor da estatística.",
            "icon": "URL ou caminho para o ícone SVG (opcional).",
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = [
            "landing_page_id",
            "text",
            "author_name",
            "author_title",
            "author_photo",
        ]
        widgets = {
            "landing_page_id": forms.Select(attrs={"class": "form-control"}),
            "text": forms.Textarea(
                attrs={"class": "form-control", "rows": 3},
            ),
            "author_name": forms.TextInput(attrs={"class": "form-control"}),
            "author_title": forms.TextInput(attrs={"class": "form-control"}),
            "author_photo": forms.FileInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "landing_page_id": "Selecione a página de destino associada ao depoimento.",
            "text": "Digite o texto do depoimento.",
            "author_name": "Digite o nome do autor do depoimento.",
            "author_title": "Digite o título do autor (opcional).",
            "author_photo": "Carregue uma foto do autor (opcional).",
        }


class ValuePropositionForm(forms.ModelForm):
    class Meta:
        model = ValueProposition
        fields = [
            "landing_page_id",
            "icon",
            "title",
            "text",
            "value",
            "frequency",
        ]
        widgets = {
            "landing_page_id": forms.Select(attrs={"class": "form-control"}),
            "icon": forms.TextInput(attrs={"class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "text": forms.Textarea(attrs={"class": "form-control"}),
            "value": forms.NumberInput(attrs={"class": "form-control"}),
            "frequency": forms.TextInput(attrs={"class": "form-control"}),
        }
        help_texts = {
            "landing_page_id": "Selecione a página de destino associada à proposta de valor.",
            "icon": "URL ou caminho para o ícone (opcional).",
            "title": "Digite o título da proposta de valor.",
            "text": "Descreva a proposta de valor.",
            "value": "Defina o valor numérico da proposta.",
            "frequency": "Digite a frequência de aplicação do valor (ex: Mensal, Anual, Única).",
        }


class FaqForm(forms.ModelForm):
    class Meta:
        model = Faq
        fields = ["question", "answer", "landing_page_id"]
        widgets = {
            "question": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                    "placeholder": "Digite a pergunta",
                },
            ),
            "answer": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                    "placeholder": "Digite a resposta",
                },
            ),
            "landing_page_id": forms.Select(
                attrs={"class": "form-control"},
                choices=[(None, "Geral")],
            ),
        }
        labels = {
            "question": "Pergunta",
            "answer": "Resposta",
            "landing_page_id": "Camapanha",
        }
        help_texts = {
            "question": "Insira a pergunta da FAQ.",
            "answer": "Insira a resposta da FAQ.",
            "landing_page_id": "Associe esta FAQ a uma página de destino específica ou deixe em branco para que seja geral.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["landing_page_id"].choices = [(None, "Geral")]
        # + [
        #     (lp.id, lp.name) for lp in LandingPage.objects.all()
        # ]
