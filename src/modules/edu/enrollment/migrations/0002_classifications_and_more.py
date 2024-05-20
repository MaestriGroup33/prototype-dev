# Generated by Django 5.0.4 on 2024-05-11 13:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('enrollment', '0001_initial'),
        ('profiles', '0003_rename_regiao_imediata_regiaoimediata_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Classifications',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('classification', models.CharField(max_length=2)),
                ('commission', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Classificação',
                'verbose_name_plural': 'Classificações',
            },
        ),
        migrations.RenameField(
            model_name='enrollments',
            old_name='campaign_id',
            new_name='campaign',
        ),
        migrations.RenameField(
            model_name='enrollments',
            old_name='course_id',
            new_name='course',
        ),
        migrations.RenameField(
            model_name='enrollments',
            old_name='student_id',
            new_name='student',
        ),
        migrations.RemoveField(
            model_name='clients',
            name='user_speech_id',
        ),
        migrations.AddField(
            model_name='clients',
            name='promoter_id',
            field=models.ForeignKey(default=1, help_text='Tutor responsável pelo aluno.', on_delete=django.db.models.deletion.CASCADE, related_name='tutor_responsible', to='profiles.profile', verbose_name='Tutor Responsável'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollments',
            name='duration_months',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollments',
            name='monthly_payment_counter',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollments',
            name='monthly_value',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='enrollments',
            name='payed_enrollment_fee',
            field=models.BooleanField(default=0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clients',
            name='status',
            field=models.CharField(choices=[('LEAD', 'Lead'), ('PRE_ENROLLED', 'Aluno Pré-Matriculado'), ('ENROLLED', 'Aluno Matriculado'), ('RE_ENROLLED', 'Veterano'), ('CANCELLED', 'Cancelado'), ('SUSPENDED', 'Trancado'), ('TRANSFERRED', 'Transferido'), ('ALUMNI', 'Ex-Aluno'), ('BLOCKED', 'Aluno com Pendências Financeiras'), ('OTHER', 'Outro')], help_text='Status do cliente.', max_length=16, verbose_name='Status do Cliente'),
        ),
        migrations.AlterField(
            model_name='clients',
            name='classification',
            field=models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='enrollment.classifications'),
        ),
    ]
