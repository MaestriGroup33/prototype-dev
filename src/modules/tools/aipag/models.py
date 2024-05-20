from django.db import models


class PageTemplate(models.Model):
    name = models.CharField(
        max_length=50,
        verbose_name="Nome do modelo",
        help_text="Nome do modelo",
        default="alphapage",
    )
    description = models.TextField(
        verbose_name="Descrição do modelo",
        help_text="Descrição do modelo",
        default="Modelo protótipo, de páginas dinâmicas atualizadas por AI",
    )
    html_base = models.TextField(
        verbose_name="HTML base do modelo",
        help_text="HTML base do modelo",
        default="alpha_base.html",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Modelo base de página"
        verbose_name_plural = "Modelos base de páginas"

    def __str__(self):
        return self.name


class Destination(models.Model):
    purpose = models.CharField(
        max_length=50,
        verbose_name="Propósito principal da página",
        help_text="Propósito principal da página",
        default="Maestri.group",
    )
    description = models.TextField(
        verbose_name="Descrição da página",
        help_text="Descrição da página",
        default="Página de apresentação da Maestri.group",
    )
    template = models.ForeignKey(
        PageTemplate,
        on_delete=models.CASCADE,
        verbose_name="Modelo base da página",
        help_text="Modelo base da página",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Página de destino"
        verbose_name_plural = "Páginas de destino"

    def __str__(self):
        return self.purpose


# Demais classes podem ser refatoradas de forma similar, observando heranças e relacionamentos apropriados.


class FixedInformation(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        verbose_name="Página de destino da informação fixa",
        help_text="Página de destino da informação fixa",
    )
    favicon = models.ImageField(
        upload_to="favicon/",
        verbose_name="Ícone da página",
        help_text="Ícone da página",
        default="favicon.png",
    )
    domain = models.CharField(
        max_length=50,
        verbose_name="Domínio da página",
        help_text="Domínio da página",
        default="maestri.group",
    )
    facebook = models.URLField(
        max_length=200,
        verbose_name="Facebook da página",
        help_text="Facebook da página",
        default="https://www.facebook.com/maestri.group",
    )
    instagram = models.URLField(
        max_length=200,
        verbose_name="Instagram da página",
        help_text="Instagram da página",
        default="https://www.instagram.com/maestri.group",
    )
    whatsapp = models.URLField(
        max_length=200,
        verbose_name="Whatsapp da página",
        help_text="Whatsapp da página",
        default="https://api.whatsapp.com/send?phone=558003333099",
    )

    class Meta:
        verbose_name = "Informação fixa da página"
        verbose_name_plural = "Informações fixas das páginas"

    def __str__(self):
        return f"{self.destination.purpose} - Fixed Information"


class Logo(models.Model):
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        verbose_name="Página de destino do logotipo",
        help_text="Página de destino do logotipo",
    )
    logo = models.ImageField(
        upload_to="logo/",
        verbose_name="Logotipo da página",
        help_text="Logotipo da página",
        default="logo.png",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Logotipo da página"
        verbose_name_plural = "Logotipos da página"

    def __str__(self):
        return f"Logo for {self.destination.purpose}"


class Version(models.Model):
    template = models.ForeignKey(
        PageTemplate,
        on_delete=models.CASCADE,
        verbose_name="Modelo base da versão",
        help_text="Modelo base da versão",
    )
    destination = models.ForeignKey(
        Destination,
        on_delete=models.CASCADE,
        verbose_name="Página de destino da versão",
        help_text="Página de destino da versão",
    )
    version = models.CharField(
        max_length=50,
        verbose_name="Versão",
        help_text="Versão",
        default="0.0.1",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Versão da página"
        verbose_name_plural = "Versões das páginas"

    def __str__(self):
        return f"Version {self.version} for {self.destination.purpose}"


class HtmlBase(models.Model):
    version = models.ForeignKey(
        Version,
        on_delete=models.CASCADE,
        verbose_name="Versão do HTML",
        help_text="Versão do HTML",
    )
    html_content = models.TextField(
        verbose_name="HTML do modelo",
        help_text="HTML do modelo",
        default="<div></div>",
    )
    theme_color = models.CharField(
        max_length=7,
        verbose_name="Cor do tema",
        help_text="Cor do tema",
        default="#000000",
    )
    title = models.CharField(
        max_length=50,
        verbose_name="Título da página",
        help_text="Título da página",
        default="Maestri.group",
    )
    description = models.TextField(
        verbose_name="Descrição da página",
        help_text="Descrição da página",
        default="Página de apresentação da Maestri.group",
    )
    keywords = models.TextField(
        verbose_name="Palavras-chave da página",
        help_text="Palavras-chave da página",
        default="Maestri, group, maestri.group",
    )
    author = models.CharField(
        max_length=50,
        verbose_name="Autor da página",
        help_text="Autor da página",
        default="Maestri.group",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Modelo base do HTML"
        verbose_name_plural = "Modelos base do HTML"

    def __str__(self):
        return self.title


class Style(models.Model):
    html_base = models.ForeignKey(
        HtmlBase,
        on_delete=models.CASCADE,
        verbose_name="Modelo base do estilo",
        help_text="Modelo base do estilo",
    )
    css = models.TextField(
        verbose_name="Caminho do CSS",
        help_text="Caminho do arquivo CSS",
        default="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Estilo CSS"
        verbose_name_plural = "Estilos CSS"

    def __str__(self):
        return f"CSS for {self.html_base.title}"


class Script(models.Model):
    html_base = models.ForeignKey(
        HtmlBase,
        on_delete=models.CASCADE,
        verbose_name="HTML base para o script",
        help_text="HTML base para o script",
    )
    script = models.TextField(
        verbose_name="Script",
        help_text="Script do modelo",
        default="https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js",
    )
    created = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de criação",
        help_text="Data de criação",
    )

    class Meta:
        verbose_name = "Script da página"
        verbose_name_plural = "Scripts das páginas"

    def __str__(self):
        return f"Script for {self.html_base.title}"
