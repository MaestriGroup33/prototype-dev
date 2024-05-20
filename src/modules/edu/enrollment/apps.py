from django.apps import AppConfig


class EnrollmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.modules.edu.enrollment"
    verbose_name = (
        "Matrículas - Gerenciamento de matrículas de alunos nos cursos da Maestri.edu"
    )
