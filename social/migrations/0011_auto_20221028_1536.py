# Generated by Django 3.2.16 on 2022-10-28 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0010_alter_review_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='report',
            name='title',
        ),
        migrations.RemoveField(
            model_name='review',
            name='title',
        ),
    ]
