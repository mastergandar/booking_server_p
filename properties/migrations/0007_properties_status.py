# Generated by Django 3.2.16 on 2022-10-27 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0006_auto_20221024_1707'),
    ]

    operations = [
        migrations.AddField(
            model_name='properties',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Published'), (1, 'Archived'), (2, 'Draft')], default=0, verbose_name='Status'),
        ),
    ]
