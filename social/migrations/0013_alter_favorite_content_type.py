# Generated by Django 3.2.16 on 2022-11-07 15:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('social', '0012_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favorite',
            name='content_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_type', to='contenttypes.contenttype'),
        ),
    ]
