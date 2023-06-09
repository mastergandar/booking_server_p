# Generated by Django 3.2.15 on 2022-10-13 12:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contenttypes', '0002_remove_content_type_name'),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Review', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='report',
            name='content_type',
            field=models.ForeignKey(limit_choices_to=models.Q(models.Q(('app_label', 'properties'), ('model', 'properties')), models.Q(('app_label', 'users'), ('model', 'user')), _connector='OR'), on_delete=django.db.models.deletion.CASCADE, related_name='report', to='contenttypes.contenttype'),
        ),
        migrations.AddField(
            model_name='report',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Report', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='notify',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notifies', to=settings.AUTH_USER_MODEL),
        ),
    ]
