# Generated by Django 3.1.6 on 2021-09-15 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0022_auto_20210910_1613'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaloperacao',
            name='numero_civis_mortos_npap',
        ),
        migrations.RemoveField(
            model_name='historicaloperacao',
            name='numero_mortes_interv_estado',
        ),
        migrations.RemoveField(
            model_name='operacao',
            name='numero_civis_mortos_npap',
        ),
        migrations.RemoveField(
            model_name='operacao',
            name='numero_mortes_interv_estado',
        ),
        migrations.AlterField(
            model_name='historicaloperacao',
            name='situacao',
            field=models.CharField(choices=[('incompleto', 'Incompleto'), ('completo', 'Completo sem Ocorrência'), ('completo com ocorrencia', 'Completo com Ocorrência')], default='incompleto', max_length=100, verbose_name='Situação Cadastro'),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='situacao',
            field=models.CharField(choices=[('incompleto', 'Incompleto'), ('completo', 'Completo sem Ocorrência'), ('completo com ocorrencia', 'Completo com Ocorrência')], default='incompleto', max_length=100, verbose_name='Situação Cadastro'),
        ),
    ]