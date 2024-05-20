from django.db import models


class Background(models.Model):
    image = models.ImageField(
        upload_to="images/",
        verbose_name="Imagem",
        help_text="Imagem carregada",
    )
    color = models.CharField(
        max_length=255,
        verbose_name="Cor",
        help_text="Cor predominante na imagem",
    )
    description = models.CharField(
        max_length=255,
        verbose_name="Descrição",
        help_text="Descrição por extenso da imagem",
    )
    url = models.CharField(
        max_length=255,
        verbose_name="URL",
        help_text="Link para a imagem",
    )
    width = models.IntegerField(verbose_name="Largura", help_text="Largura da imagem")
    height = models.IntegerField(verbose_name="Altura", help_text="Altura da imagem")
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Criado em",
        help_text="Data de criação da imagem",
    )

    class Meta:
        verbose_name = "Background"
        verbose_name_plural = "Backgrounds"

    def __str__(self):
        # Represent the model instance as the datetime it was created
        return self.created_at.strftime("%Y-%m-%d %H:%M:%S")
