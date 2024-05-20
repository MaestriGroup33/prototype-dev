from django.contrib import messages
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from rest_framework import filters
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination

from .forms import CardForm
from .forms import FaqForm
from .forms import LandingPageForm
from .forms import SectionForm
from .forms import StatisticForm
from .forms import TestimonialForm
from .forms import ValuePropositionForm
from .models import Card
from .models import Faq
from .models import LandingPage
from .models import Section
from .models import Statistic
from .models import Testimonial
from .models import ValueProposition
from .serializers import CardSerializer
from .serializers import FaqSerializer
from .serializers import LandingPageSerializer
from .serializers import SectionSerializer
from .serializers import StatisticSerializer
from .serializers import TestimonialSerializer
from .serializers import ValuePropositionSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class LandingPageViewSet(viewsets.ModelViewSet):
    """
    A viewset that provides the standard actions to manage Landing Pages.
    Includes searching, filtering, and ordering features.
    """

    queryset = LandingPage.objects.all()
    serializer_class = LandingPageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["name", "active"]
    search_fields = ["name", "campaign_start", "campaign_end"]
    ordering_fields = ["name", "campaign_start", "campaign_end"]
    pagination_class = StandardResultsSetPagination

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]


class SectionViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing sections.
    Includes filtering, search, and ordering capabilities.
    """

    queryset = Section.objects.select_related("landing_page_id").all()
    serializer_class = SectionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["landing_page_id", "title"]
    search_fields = ["title", "subtitle", "text"]
    ordering_fields = ["title", "subtitle"]
    pagination_class = StandardResultsSetPagination


class CardViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing cards within sections.
    Includes filters and pagination.
    """

    queryset = Card.objects.select_related("section").all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = []
    filterset_fields = ["section", "title"]
    pagination_class = StandardResultsSetPagination


class StatisticViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing statistics associated with sections.
    Includes search and ordering functionalities.
    """

    queryset = Statistic.objects.select_related("section").all()
    serializer_class = StatisticSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    search_fields = ["title"]
    ordering_fields = ["title", "value"]
    pagination_class = StandardResultsSetPagination


class TestimonialViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing testimonials on landing pages.
    Includes extensive filtering and search capabilities.
    """

    queryset = Testimonial.objects.select_related("landing_page_id").all()
    serializer_class = TestimonialSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["landing_page_id", "author_name"]
    search_fields = ["text", "author_name", "author_title"]
    ordering_fields = ["author_name"]
    pagination_class = StandardResultsSetPagination


class ValuePropositionViewSet(viewsets.ModelViewSet):
    """
    A viewset for managing value propositions associated with landing pages.
    Includes pagination and filtering.
    """

    queryset = ValueProposition.objects.select_related("landing_page_id").all()
    serializer_class = ValuePropositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = []
    filterset_fields = ["landing_page_id", "title"]
    pagination_class = StandardResultsSetPagination


class FaqViewSet(viewsets.ModelViewSet):
    queryset = Faq.objects.select_related("landing_page_id").all()
    serializer_class = FaqSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = []
    filterset_fields = ["landing_page_id", "title"]


# vamos definir views para os formulários


class LandingPageFormView(FormView):
    template_name = "landing_page_form.html"
    form_class = LandingPageForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Landing Page salva com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


class SectionFormView(FormView):
    template_name = "section_form.html"
    form_class = SectionForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Seção salva com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


class CardFormView(FormView):
    template_name = "card_form.html"
    form_class = CardForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Card salvo com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


class StatisticFormView(FormView):
    template_name = "statistic_form.html"
    form_class = StatisticForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Estatística salva com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


class TestimonialFormView(FormView):
    template_name = "testimonial_form.html"
    form_class = TestimonialForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Testemunho salvo com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


class ValuePropositionFormView(FormView):
    template_name = "value_proposition_form.html"
    form_class = ValuePropositionForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "Proposta de valor salva com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


class FaqFormView(FormView):
    template_name = "faq_form.html"
    form_class = FaqForm
    success_url = reverse_lazy("success")  # Altere para a URL de sucesso desejada

    def form_valid(self, form):
        # Aqui você pode processar os dados do formulário como necessário
        form.save()  # Salva o modelo se o formulário for ModelForm
        messages.success(self.request, "FAQ salvo com sucesso!")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(
            self.request,
            "O formulário contém erros. Por favor, corrija-os.",
        )
        return super().form_invalid(form)


def landing_page_form(request):
    if request.method == "POST":
        form = LandingPageForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Landing Page salva com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = LandingPageForm()

    return render(request, "landing_page_form.html", {"form": form})


def section_form(request):
    if request.method == "POST":
        form = SectionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Seção salva com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = SectionForm()

    return render(request, "section_form.html", {"form": form})


def card_form(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Card salvo com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = CardForm()

    return render(request, "card_form.html", {"form": form})


def statistic_form(request):
    if request.method == "POST":
        form = StatisticForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Estatística salva com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = StatisticForm()

    return render(request, "statistic_form.html", {"form": form})


def testimonial_form(request):
    if request.method == "POST":
        form = TestimonialForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Testemunho salvo com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = TestimonialForm()

    return render(request, "testimonial_form.html", {"form": form})


def value_proposition_form(request):
    if request.method == "POST":
        form = ValuePropositionForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Proposta de valor salva com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = ValuePropositionForm()

    return render(request, "value_proposition_form.html", {"form": form})


def faq_form(request):
    if request.method == "POST":
        form = FaqForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "FAQ salvo com sucesso!")
            return redirect("success")  # Altere para a URL de sucesso desejada
    else:
        form = FaqForm()

    return render(request, "faq_form.html", {"form": form})


def success(request):
    return render(request, "success.html")
