# Generated by Django 5.0.4 on 2024-05-01 02:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unsplash', '0003_alter_background_options_remove_background_color_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='background',
            options={'verbose_name': 'Background', 'verbose_name_plural': 'Backgrounds'},
        ),
        migrations.RemoveField(
            model_name='background',
            name='image_file',
        ),
        migrations.AddField(
            model_name='background',
            name='color',
            field=models.CharField(default=11, help_text='Cor predominante na imagem', max_length=255, verbose_name='Cor'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now, help_text='Data de criação da imagem', verbose_name='Criado em'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='description',
            field=models.CharField(default=1, help_text='Descrição por extenso da imagem', max_length=255, verbose_name='Descrição'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='height',
            field=models.IntegerField(default=1, help_text='Altura da imagem', verbose_name='Altura'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='image',
            field=models.ImageField(default=1, help_text='Imagem carregada', upload_to='images/', verbose_name='Imagem'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='background',
            name='width',
            field=models.IntegerField(default=1, help_text='Largura da imagem', verbose_name='Largura'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='background',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='background',
            name='url',
            field=models.CharField(help_text='Link para a imagem', max_length=255, verbose_name='URL'),
        ),
    ]
