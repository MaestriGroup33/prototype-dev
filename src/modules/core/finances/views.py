# Create your views here.
from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from rest_framework import permissions
from rest_framework import viewsets

from .forms import GlobalSettingsForm
from .forms import IndicatorsForm
from .models import GlobalSettings
from .models import Indicators
from .serializers import GlobalSettingsSerializer
from .serializers import IndicatorsSerializer


class GlobalSettingsViewSet(viewsets.ModelViewSet):
    queryset = GlobalSettings.objects.all()
    serializer_class = GlobalSettingsSerializer
    permission_classes = [permissions.IsAuthenticated]


class GlobalSettingsFormView(FormView):
    template_name = "global_settings_form.html"
    form_class = GlobalSettingsForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Configurações globais salvas com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


def global_settings_form(request):
    if request.method == "POST":
        form = GlobalSettingsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Configurações globais salvas com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = GlobalSettingsForm()

    return render(request, "global_settings_form.html", {"form": form})


class IndicatorsViewSet(viewsets.ModelViewSet):
    queryset = Indicators.objects.all()
    serializer_class = IndicatorsSerializer
    permission_classes = [permissions.IsAuthenticated]


class IndicatorsFormView(FormView):
    template_name = "indicators_form.html"
    form_class = IndicatorsForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Indicadores salvos com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


def indicators_form(request):
    if request.method == "POST":
        form = IndicatorsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Indicadores salvos com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = IndicatorsForm()

    return render(request, "indicators_form.html", {"form": form})
