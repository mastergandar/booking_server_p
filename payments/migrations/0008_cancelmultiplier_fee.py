# Generated by Django 3.2.16 on 2022-10-31 13:11

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0007_alter_orders_created_at'),
    ]

    operations = [
        migrations.CreateModel(
            name='CancelMultiplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount_168', models.FloatField(verbose_name='Amount 168h+')),
                ('amount_72', models.FloatField(verbose_name='Amount 168h-72h')),
                ('amount_24', models.FloatField(verbose_name='Amount 72h-24h')),
                ('amount_0', models.FloatField(verbose_name='Amount last 24h')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Fee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version', models.IntegerField(default=1, verbose_name='Version')),
                ('is_main', models.BooleanField(default=False, verbose_name='Is main')),
                ('amount', models.IntegerField(default=0, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Amount')),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
