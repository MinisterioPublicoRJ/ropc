# Generated by Django 3.1.6 on 2021-03-04 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0003_auto_20210304_1338'),
    ]

    operations = [
        migrations.RenameField(
            model_name='operacao',
            old_name='numero_adolescentes_apreendindos',
            new_name='numero_adolescentes_apreendidos',
        ),
    ]
