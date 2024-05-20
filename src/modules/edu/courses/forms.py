# forms referente ao courses, um para adicionar novos cursos outro para visualizar os cursos

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = "__all__"
        labels = {
            "cod": _("Código"),
            "name": _("Nome"),
            "description": _("Descrição"),
            "duration": _("Duração"),
            "type": _("Tipo"),
            "area": _("Área"),
            "information": _("Informações"),
            "objective": _("Objetivo"),
            "jobmarket": _("Mercado de Trabalho"),
            "specifics": _("Informações Específicas"),
            "curriculum": _("Grade Curricular"),
            "avatar": _("Avatar"),
        }
        help_texts = {
            "cod": _(
                "Código do Curso, exemplo: adm-administração, mpr-Ministério Pastoral...",
            ),
            "name": _("Nome do curso"),
            "description": _("Descrição do curso"),
            "duration": _("Duração do curso"),
            "type": _("Tipo do curso"),
            "area": _("Área do curso"),
            "information": _("Informações do curso"),
            "objective": _("Objetivo do curso"),
            "jobmarket": _("Mercado de Trabalho"),
            "specifics": _("Informações Específicas"),
            "curriculum": _("Grade Curricular"),
            "avatar": _("Avatar do curso"),
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "information": forms.Textarea(attrs={"rows": 3}),
            "objective": forms.Textarea(attrs={"rows": 3}),
            "jobmarket": forms.Textarea(attrs={"rows": 3}),
            "specifics": forms.Textarea(attrs={"rows": 3}),
            "curriculum": forms.Textarea(attrs={"rows": 3}),
        }


class CourseSearchForm(forms.Form):
    q = forms.CharField(
        label=_("Pesquisar"),
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"placeholder": _("Pesquisar...")}),
    )

    # forms para pesquisar cursos
