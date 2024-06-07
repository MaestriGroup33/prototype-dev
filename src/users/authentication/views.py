import re
from django.utils.translation import gettext_lazy as _
from src.users.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from rest_framework.decorators import authentication_classes, permission_classes
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
@authentication_classes([])
@permission_classes([])
def login_view(request):
    if request.method == "POST":
        print(request.POST)
        cpf = request.POST["cpf"]
        password = request.POST["password"]
        cpf_format = re.sub(r"[^0-9]", "", cpf)
        print(cpf)
        print(password)
        user = authenticate(request, cpf=cpf_format, password=password)
        print(user)
        if user is not None:
            login(request, user)
            print("entrou aqui")
            # Autenticação bem-sucedida, redirecione para a página de sucesso ou faça o que for necessário
            return redirect("/app")
            # Autenticação falhou, lide com isso de acordo
    # Renderize o formulário de login
    return render(request, "pages/login.html")


@csrf_exempt
@authentication_classes([])
@permission_classes([])
def register(request):
    form = UserCreationForm()
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            user.is_valid = False
            user.save()

            return redirect("mysite")

        else:
            print("invalid registration details")

    return render(request, "pages/register.html", {"form": form})
