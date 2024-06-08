# Generated by Django 4.2.13 on 2024-05-23 13:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(help_text='Código do Curso, exemplo: adm-administração, mpr-Ministério Pastoral...', max_length=255, verbose_name='Código')),
                ('name', models.CharField(help_text='Nome do curso', max_length=255, verbose_name='Nome')),
                ('description', models.TextField(help_text='Descrição do curso', verbose_name='Descrição')),
                ('duration', models.CharField(choices=[('12', '2 Semestres'), ('18', '3 Semestres'), ('24', '4 Semestres'), ('30', '5 Semestres'), ('36', '6 Semestres'), ('42', '7 Semestres'), ('48', '8 Semestres'), ('54', '9 Semestres'), ('60', '10 Semestres')], help_text='Duração do curso', max_length=2, verbose_name='Duração')),
                ('type', models.CharField(choices=[('tec', 'Tecnólogo'), ('r2', 'Licenciatura R2'), ('bch', 'Bacharelado'), ('lic', 'Licenciatura'), ('pg', 'Formação Pedagógica')], help_text='Tipo do curso', max_length=3, verbose_name='Tipo')),
                ('area', models.CharField(choices=[('adm', 'Administração'), ('cj', 'Ciências Jurídicas'), ('dp', 'Desenvolvimento Pessoal'), ('edu', 'Educação'), ('ead', 'Educação EAD'), ('ea', 'Engenharia e Arquitetura'), ('fv', 'Fotografia e Vídeo'), ('gn', 'Gestão e Negócios'), ('ip', 'Indicação Profissional'), ('mc', 'Marketing e Comunicação'), ('rh', 'Recursos Humanos'), ('sb', 'Saúde e Bem-estar'), ('tec', 'Tecnologia'), ('ti', 'Tecnologia da Informação'), ('pg', 'Formação Pedagógica')], help_text='Área do curso', max_length=3, verbose_name='Área')),
                ('information', models.TextField(help_text='Informações do curso', verbose_name='Informações')),
                ('objective', models.TextField(help_text='Objetivo do curso', verbose_name='Objetivo')),
                ('jobmarket', models.TextField(help_text='Mercado de Trabalho', verbose_name='Mercado de Trabalho')),
                ('specifics', models.TextField(help_text='Informações Específicas', verbose_name='Informações Específicas')),
                ('curriculum', models.TextField(help_text='Grade Curricular', verbose_name='Grade Curricular')),
                ('avatar', models.ImageField(help_text='Avatar do curso', upload_to='courses', verbose_name='Avatar')),
            ],
            options={
                'verbose_name': 'Curso',
                'verbose_name_plural': 'Cursos',
                'ordering': ('name',),
            },
        ),
        migrations.CreateModel(
            name='CourseReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Nome')),
                ('email', models.EmailField(max_length=254, verbose_name='E-mail')),
                ('review', models.TextField(verbose_name='Avaliação')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='courses.course')),
            ],
            options={
                'verbose_name': 'Avaliação',
                'verbose_name_plural': 'Avaliações',
                'ordering': ('-created_at',),
            },
        ),
    ]
