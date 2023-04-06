# Generated by Django 3.2.16 on 2022-10-18 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_auto_20221014_1503'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='rejected_type',
            field=models.SmallIntegerField(blank=True, choices=[(0, 'Changed your mind'), (1, 'Found another place to live'), (2, 'Changed the route'), (3, 'Circumstances have changed'), (4, 'Another reason'), (5, 'Property owner changed terms')], null=True, verbose_name='Rejected type'),
        ),
    ]
