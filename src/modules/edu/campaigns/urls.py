from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CardFormView
from .views import CardViewSet
from .views import FaqFormView
from .views import FaqViewSet
from .views import LandingPageFormView
from .views import LandingPageViewSet
from .views import SectionFormView
from .views import SectionViewSet
from .views import StatisticFormView
from .views import StatisticViewSet
from .views import TestimonialFormView
from .views import TestimonialViewSet
from .views import ValuePropositionFormView
from .views import ValuePropositionViewSet
from .views import card_form
from .views import faq_form
from .views import landing_page_form
from .views import section_form
from .views import statistic_form
from .views import success
from .views import testimonial_form
from .views import value_proposition_form

# Criar um router e registrar nossos viewsets com ele
router = DefaultRouter()
router.register(r"landingpages", LandingPageViewSet, basename="landingpage")
router.register(r"sections", SectionViewSet, basename="section")
router.register(r"cards", CardViewSet, basename="card")
router.register(r"statistics", StatisticViewSet, basename="statistic")
router.register(r"testimonials", TestimonialViewSet, basename="testimonial")
router.register(
    r"valuepropositions",
    ValuePropositionViewSet,
    basename="valueproposition",
)
router.register(r"faqs", FaqViewSet, basename="faq")

app_name = "modules.edu.campaigns"

urlpatterns = [
    path("", include(router.urls)),
    path("landing-page/", LandingPageFormView.as_view(), name="landingpage_form"),
    path("landing-page-func/", landing_page_form, name="landingpage_form_func"),
    path("section/", SectionFormView.as_view(), name="section_form"),
    path("section-func/", section_form, name="section_form_func"),
    path("card/", CardFormView.as_view(), name="card_form"),
    path("card-func/", card_form, name="card_form_func"),
    path("statistic/", StatisticFormView.as_view(), name="statistic_form"),
    path("statistic-func/", statistic_form, name="statistic_form_func"),
    path("testimonial/", TestimonialFormView.as_view(), name="testimonial_form"),
    path("testimonial-func/", testimonial_form, name="testimonial_form_func"),
    path(
        "value-proposition/",
        ValuePropositionFormView.as_view(),
        name="valueproposition_form",
    ),
    path(
        "value-proposition-func/",
        value_proposition_form,
        name="valueproposition_form_func",
    ),
    path("faq/", FaqFormView.as_view(), name="faq_form"),
    path("faq-func/", faq_form, name="faq_form_func"),
    path("success/", success, name="success"),
]
