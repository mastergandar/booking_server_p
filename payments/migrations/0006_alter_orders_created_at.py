# Generated by Django 3.2.16 on 2022-10-27 13:17

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_orders_rejected_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2022, 10, 27, 13, 17, 21, 688552, tzinfo=utc), editable=False),
        ),
    ]
