# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from src.modules.tools.mercado_pago.models import MercadoPagoDetails
from src.modules.tools.mercado_pago import secrets as mp_secrets
from src.users.models import User


@login_required
def edit_promo(request):

    user: User = request.user

    if user is None:
        return render(request, "app/edit_promo_code.html")

    if request.method == "POST":
        return render(request, "app/edit_promo_code.html")

    if user.profile is not None:
        code = user.profile.promotional_code

    context = {"promo_code": code}

    return render(request, "app/edit_promo_code.html", context)


@login_required
def finances(request):
    user: User = request.user

    context = {"mp": False, "msg": "", "link": mp_secrets.mp_integration}

    if user.profile is not None:
        try:
            mp = MercadoPagoDetails.objects.get(promoter=user.profile)
            context["mp"] = True
        except MercadoPagoDetails.DoesNotExist:
            context["msg"] = "Por favor complete sua integração com o MercadoPago"

    return render(request, "app/finances.html", context)
