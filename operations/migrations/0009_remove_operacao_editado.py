# Generated by Django 3.1.6 on 2021-03-11 20:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('operations', '0008_merge_20210311_1257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='operacao',
            name='editado',
        ),
    ]
