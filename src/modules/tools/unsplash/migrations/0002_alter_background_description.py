# Generated by Django 5.0.4 on 2024-04-17 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unsplash', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='background',
            name='description',
            field=models.CharField(blank=True, help_text='Descrição por extenso da imagem', max_length=255, null=True, verbose_name='Descrição'),
        ),
    ]
