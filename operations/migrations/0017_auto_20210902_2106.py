# Generated by Django 3.1.6 on 2021-09-03 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0016_auto_20210902_2009'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicaloperacao',
            name='comunicou_escolas_saude',
            field=models.BooleanField(blank=True, null=True, verbose_name='Comunicou a equipamentos de saúde e escolas?'),
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='escolas_perto',
            field=models.BooleanField(blank=True, null=True, verbose_name='Escolas nas proximidades?'),
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='hospitais_perto',
            field=models.BooleanField(blank=True, null=True, verbose_name='Hospitais nas proximidades?'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='comunicou_escolas_saude',
            field=models.BooleanField(blank=True, null=True, verbose_name='Comunicou a equipamentos de saúde e escolas?'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='escolas_perto',
            field=models.BooleanField(blank=True, null=True, verbose_name='Escolas nas proximidades?'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='hospitais_perto',
            field=models.BooleanField(blank=True, null=True, verbose_name='Hospitais nas proximidades?'),
        ),
    ]
