# Generated by Django 3.1 on 2023-11-29 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0028_auto_20230831_1342'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicaloperacao',
            name='comunicou_escolas_saude',
        ),
        migrations.RemoveField(
            model_name='historicaloperacao',
            name='descricao_analise_risco',
        ),
        migrations.RemoveField(
            model_name='historicaloperacao',
            name='hospitais_perto',
        ),
        migrations.RemoveField(
            model_name='operacao',
            name='comunicou_escolas_saude',
        ),
        migrations.RemoveField(
            model_name='operacao',
            name='descricao_analise_risco',
        ),
        migrations.RemoveField(
            model_name='operacao',
            name='hospitais_perto',
        ),
        migrations.AddField(
            model_name='historicaloperacao',
            name='comunicacao_escola',
            field=models.BooleanField(blank=True, null=True, verbose_name='Houve comunicação prévia às autoridades de educação?'),
        ),
        migrations.AddField(
            model_name='operacao',
            name='comunicacao_escola',
            field=models.BooleanField(blank=True, null=True, verbose_name='Houve comunicação prévia às autoridades de educação?'),
        ),
    ]
