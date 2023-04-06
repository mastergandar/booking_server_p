# Generated by Django 3.2.15 on 2022-10-14 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_auto_20221013_1533'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='rejected_reason',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Rejected reason'),
        ),
        migrations.AlterField(
            model_name='orders',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'Pending'), (1, 'Complete'), (2, 'Cancelled by customer'), (3, 'Cancelled by owner')], default=0, verbose_name='Status'),
        ),
    ]