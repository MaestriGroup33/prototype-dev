# views.py
from django.http import JsonResponse

from .utils import cidades_por_estado


def get_cidades(request):
    estado = request.GET.get("estado")
    cidades = cidades_por_estado(estado)
    return JsonResponse(cidades, safe=False)
