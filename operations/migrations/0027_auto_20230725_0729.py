# Generated by Django 3.1.6 on 2023-07-25 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0026_auto_20211208_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloperacao',
            name='justificativa_uso_aeronave',
            field=models.TextField(blank=True, null=True, verbose_name='Justificativa do uso de aeronave'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='justificativa_uso_aeronave',
            field=models.TextField(blank=True, null=True, verbose_name='Justificativa do uso de aeronave'),
        ),
    ]
