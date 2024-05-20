# Generated by Django 4.2.13 on 2024-05-20 18:07

from django.db import migrations, models
import src.modules.core.profiles.validators


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_rename_regiao_imediata_regiaoimediata_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='birth_date',
            field=models.DateField(help_text='Data de Nascimento', validators=[src.modules.core.profiles.validators.validate_birthdate], verbose_name='Data de Nascimento'),
        ),
    ]
