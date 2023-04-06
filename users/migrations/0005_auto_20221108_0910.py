# Generated by Django 3.2.16 on 2022-11-08 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_user_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='activation_email_code',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Email confirmation code'),
        ),
        migrations.AddField(
            model_name='user',
            name='email_activation_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
