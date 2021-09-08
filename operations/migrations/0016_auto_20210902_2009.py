# Generated by Django 3.1.6 on 2021-09-02 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0015_auto_20210901_2247'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operacao',
            name='localidade_operacao',
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='bairro',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='endereco_referencia',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço de referência'),
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='localidade',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Localidade'),
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='municipio',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Município'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='bairro',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Bairro'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='endereco_referencia',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Endereço de referência'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='localidade',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Localidade'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='municipio',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Município'),
        ),
    ]
