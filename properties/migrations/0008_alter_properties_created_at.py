# Generated by Django 3.2.16 on 2022-10-27 13:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('properties', '0007_properties_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='properties',
            name='created_at',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2022, 10, 27, 13, 17, 21, 708006, tzinfo=utc), null=True, verbose_name='Created at'),
        ),
    ]