# Generated by Django 3.1.6 on 2021-03-09 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0005_auto_20210309_1403'),
    ]

    operations = [
        migrations.AddField(
            model_name='operacao',
            name='completo',
            field=models.BooleanField(default=False, verbose_name='Cadastro Completo'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='situacao',
            field=models.CharField(choices=[('incompleto', 'Incompleto'), ('completo sem ocorrencia', 'Completo sem Ocorrência'), ('completo com ocorrencia', 'Completo com Ocorrência')], default='incompleto', max_length=100, verbose_name='Situação Cadastro'),
        ),
    ]
