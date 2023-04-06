# Generated by Django 3.2.15 on 2022-10-13 12:38

import core.file_storage
import core.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Amenities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to=core.file_storage.amenities_image_file_path, validators=[core.validators.validate_images_file_max_size], verbose_name='Image')),
                ('tittle', models.CharField(max_length=250, verbose_name='Tittle')),
            ],
        ),
        migrations.CreateModel(
            name='AmenitiesBinding',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('custom_amenity', models.CharField(blank=True, max_length=250, null=True, verbose_name='Amenity')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('map_id', models.CharField(blank=True, max_length=80, null=True, verbose_name='Map_Id')),
                ('country', models.CharField(max_length=40, verbose_name='Country')),
                ('city', models.CharField(max_length=60, verbose_name='City')),
                ('street', models.CharField(blank=True, max_length=60, null=True, verbose_name='Street')),
            ],
        ),
        migrations.CreateModel(
            name='Properties',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tittle', models.CharField(max_length=250, verbose_name='Tittle')),
                ('accommodation_type', models.SmallIntegerField(choices=[(0, 'House'), (1, 'Flat'), (2, 'Room'), (3, 'Unique'), (4, 'Hotel')], verbose_name='Accommodation')),
                ('flat_type', models.SmallIntegerField(blank=True, choices=[(0, 'Atelier'), (1, 'Apartment'), (2, 'Loft')], null=True, verbose_name='Type')),
                ('house_type', models.SmallIntegerField(blank=True, choices=[(0, 'House'), (1, 'Country house'), (2, 'Cottage'), (3, 'Townhouse')], null=True, verbose_name='Accommodation')),
                ('room_type', models.SmallIntegerField(blank=True, choices=[(0, 'Room with amenities'), (1, 'Room in apartment'), (2, 'Bed in common room')], null=True, verbose_name='Accommodation')),
                ('unique_type', models.SmallIntegerField(blank=True, choices=[(0, 'Transport'), (1, 'Natural'), (2, 'Tower'), (3, 'Other')], null=True, verbose_name='Accommodation')),
                ('hotel_type', models.SmallIntegerField(blank=True, choices=[(0, 'Hotel'), (1, 'Hostel'), (2, 'Resort'), (3, 'B&B'), (4, 'Apart-hotel')], null=True, verbose_name='Accommodation')),
                ('rent_type', models.SmallIntegerField(choices=[(0, 'Individual'), (1, 'Company')], verbose_name='Rent type')),
                ('guests_count', models.IntegerField(verbose_name='Guests count')),
                ('beds_count', models.IntegerField(verbose_name='Beds count')),
                ('bedrooms_count', models.IntegerField(verbose_name='Bedrooms count')),
                ('bathrooms_count', models.IntegerField(verbose_name='Bathrooms count')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_available', models.BooleanField(default=True, verbose_name='Available')),
                ('additional_rules', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), blank=True, null=True, size=None)),
                ('unavailable_from', models.DateTimeField(blank=True, null=True, verbose_name='Unavailable from')),
                ('unavailable_to', models.DateTimeField(blank=True, null=True, verbose_name='Unavailable to')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(auto_now=True, null=True, verbose_name='Updated at')),
            ],
        ),
        migrations.CreateModel(
            name='Rules',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('children', models.BooleanField(default=True, verbose_name='Children')),
                ('suitable_for_babies', models.BooleanField(default=True, verbose_name='Suitable for babies')),
                ('pets', models.BooleanField(default=True, verbose_name='Pets')),
                ('smoking', models.BooleanField(default=True, verbose_name='Smoking')),
                ('parties', models.BooleanField(default=True, verbose_name='Parties')),
            ],
        ),
        migrations.CreateModel(
            name='PropertyImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to=core.file_storage.property_image_file_path, validators=[core.validators.validate_images_file_max_size], verbose_name='Property image')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_images', to='properties.properties')),
            ],
        ),
        migrations.AddField(
            model_name='properties',
            name='rules',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Properties', to='properties.rules'),
        ),
    ]