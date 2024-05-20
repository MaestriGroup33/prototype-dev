from django.apps import AppConfig


class EduConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.edu"
    verbose_name = "Educação - Gerenciamento de cursos, campanhas, cobranças e alunos da Maestri.edu"
