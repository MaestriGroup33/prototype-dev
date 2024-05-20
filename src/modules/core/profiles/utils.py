import requests
from django.db import models
from django.http import JsonResponse
from django.urls import path


class Regiao(models.Model):
    id = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.nome} ({self.sigla})"


class Estado(models.Model):
    id = models.IntegerField(primary_key=True)
    sigla = models.CharField(max_length=2)
    nome = models.CharField(max_length=50)
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Mesorregiao(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    UF = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class Microrregiao(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    mesorregiao = models.ForeignKey(Mesorregiao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class RegiaoIntermediaria(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    UF = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


class RegiaoImediata(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    regiao_intermediaria = models.ForeignKey(
        RegiaoIntermediaria,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.nome


class Municipio(models.Model):
    id = models.IntegerField(primary_key=True)
    nome = models.CharField(max_length=50)
    microrregiao = models.ForeignKey(Microrregiao, on_delete=models.CASCADE)
    regiao_imediata = models.ForeignKey(RegiaoImediata, on_delete=models.CASCADE)
    regiao_intermediaria = models.ForeignKey(
        RegiaoIntermediaria,
        on_delete=models.CASCADE,
    )
    regiao = models.ForeignKey(Regiao, on_delete=models.CASCADE)
    UF = models.ForeignKey(Estado, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome


def get_json_data():
    url = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios?orderBy=nivelado"
    response = requests.get(url, timeout=10)
    return response.json()


def save_data_to_models():
    json_data = get_json_data()

    for data in json_data:
        # Save data to municipio model
        Municipio.objects.create(
            id=data["id"],
            nome=data["nome"],
            microrregiao_id=data["microrregiao"]["id"],
            regiao_imediata_id=data["regiao_imediata"]["id"],
            regiao_intermediaria_id=data["regiao_intermediaria"]["id"],
            regiao_id=data["regiao"]["id"],
            UF_id=data["UF"]["id"],
        )

        # Save data to microrregiao model
        Microrregiao.objects.get_or_create(
            id=data["microrregiao"]["id"],
            nome=data["microrregiao"]["nome"],
            mesorregiao_id=data["microrregiao"]["mesorregiao"]["id"],
        )

        # Save data to regiao_imediata model
        RegiaoImediata.objects.get_or_create(
            id=data["regiao_imediata"]["id"],
            nome=data["regiao_imediata"]["nome"],
            regiao_intermediaria_id=data["regiao_imediata"]["regiao_intermediaria"][
                "id"
            ],
        )

        # Save data to regiao_intermediaria model
        RegiaoIntermediaria.objects.get_or_create(
            id=data["regiao_intermediaria"]["id"],
            nome=data["regiao_intermediaria"]["nome"],
            UF_id=data["regiao_intermediaria"]["UF"]["id"],
        )

        # Save data to regiao model
        Regiao.objects.get_or_create(
            id=data["regiao"]["id"],
            sigla=data["regiao"]["sigla"],
            nome=data["regiao"]["nome"],
        )

        # Save data to estado model
        Estado.objects.get_or_create(
            id=data["UF"]["id"],
            sigla=data["UF"]["sigla"],
            nome=data["UF"]["nome"],
            regiao_id=data["UF"]["regiao"]["id"],
        )


def cidades_por_estado(estado):
    cidades = Municipio.objects.filter(UF__sigla=estado).values("id", "nome")
    return list(cidades)


def get_cidades(request):
    estado = request.GET.get("estado")
    cidades = cidades_por_estado(estado)
    return JsonResponse(cidades, safe=False)


urlpatterns = [path("cidades/", get_cidades, name="get_cidades")]
