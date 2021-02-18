# Generated by Django 3.1.6 on 2021-02-18 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bairro',
            fields=[
                ('municipio', models.TextField(db_column='municipio')),
                ('bairro_id', models.CharField(db_column='bairro_id', max_length=255, primary_key=True, serialize=False)),
                ('bairro', models.TextField(db_column='bairro')),
            ],
            options={
                'db_table': '"bairros"."bairros_rj"',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('cod_6_dig', models.IntegerField(db_column='cod_6_dig', primary_key=True, serialize=False)),
                ('nm_mun', models.CharField(db_column='nm_mun', max_length=60)),
                ('cod_mun', models.CharField(db_column='cod_mun', max_length=7)),
            ],
            options={
                'db_table': '"basegeo"."lim_municipios"',
                'managed': False,
            },
        ),
    ]
