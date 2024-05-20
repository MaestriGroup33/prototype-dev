from django.urls import path

from .views import Payment
from .views import PaymentResponse
from .views import payment

app_name = "tools_mercado_pago"

urlpatterns = [
    path("payment/", payment, name="payment"),
    path("payment_test/", Payment.as_view()),
    path("payment_response/", PaymentResponse.as_view()),
]
