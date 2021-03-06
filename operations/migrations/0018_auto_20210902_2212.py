# Generated by Django 3.1.6 on 2021-09-03 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0017_auto_20210902_2106'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloperacao',
            name='numero_civis_mortos',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Número de civis mortos'),
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='numero_presos_outros_mandados',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Número de presos indicados em outros mandados de prisão pendentes'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='numero_civis_mortos',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Número de civis mortos'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='numero_presos_outros_mandados',
            field=models.PositiveIntegerField(blank=True, default=0, verbose_name='Número de presos indicados em outros mandados de prisão pendentes'),
        ),
    ]
