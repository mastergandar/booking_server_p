# Generated by Django 3.2.16 on 2022-10-24 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0004_auto_20221018_1551'),
    ]

    operations = [
        migrations.RenameField(
            model_name='properties',
            old_name='tittle',
            new_name='title',
        ),
    ]
