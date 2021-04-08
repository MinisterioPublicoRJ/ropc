# Generated by Django 3.1.6 on 2021-04-08 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0012_auto_20210312_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='historicaloperacao',
            name='nome_condutor_ocorrencia',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do condutor da ocorrência'),
        ),
        migrations.AlterField(
            model_name='historicaloperacao',
            name='objetivo_estrategico_operacao',
            field=models.TextField(blank=True, null=True, verbose_name='Objetivo estratégico da operação'),
        ),
        migrations.AlterField(
            model_name='historicaloperacao',
            name='registro_ocorrencia',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registro de Ocorrência'),
        ),
        migrations.AlterField(
            model_name='historicaloperacao',
            name='unidade_apoiadora',
            field=models.TextField(blank=True, null=True, verbose_name='Unidade Apoiadora'),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='nome_condutor_ocorrencia',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nome do condutor da ocorrência'),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='objetivo_estrategico_operacao',
            field=models.TextField(blank=True, null=True, verbose_name='Objetivo estratégico da operação'),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='registro_ocorrencia',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Registro de Ocorrência'),
        ),
        migrations.AlterField(
            model_name='operacao',
            name='unidade_apoiadora',
            field=models.TextField(blank=True, null=True, verbose_name='Unidade Apoiadora'),
        ),
    ]