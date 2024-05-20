from django import forms

from .models import Classifications


class ClassificationsForm(forms.ModelForm):
    class Meta:
        model = Classifications
        fields = "__all__"  # Inclui todos os campos do modelo Classifications
        labels = {"classificacao": "Classificação", "descricao": "Descrição"}
        help_texts = {
            "classificacao": "Insira a classificação.",
            "descricao": "Insira a descrição.",
        }
