from django.contrib import admin

from .models import Background
from .tasks import buscar_imagem_aleatoria


@admin.register(Background)
class BackgroundAdmin(admin.ModelAdmin):
    actions = ["buscar_nova_imagem"]

    def buscar_nova_imagem(self, request, queryset):
        result = print(buscar_imagem_aleatoria())
