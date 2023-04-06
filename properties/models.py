import datetime
from datetime import timedelta

from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models import QuerySet

from core.file_storage import amenities_image_file_path, property_image_file_path
from core.validators import validate_images_file_max_size
from file_manager.models import LinkedImages
from payments.models import Orders
from properties.enums import AccommodationType, HouseType, RoomType, UniqueType, HotelType, RentType, FlatType, Status
from properties.utils import list_of_days_from_data_range
from social.models import Review, Favorite


class Properties(models.Model):

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="Properties"
    )

    title = models.CharField(
        'Title',
        max_length=250,
        null=False,
        blank=False,
    )

    accommodation_type = models.SmallIntegerField(
        'Accommodation',
        choices=AccommodationType.choices,
        null=False,
        blank=False
    )

    flat_type = models.SmallIntegerField(
        'Flat type',
        choices=FlatType.choices,
        null=True,
        blank=True
    )

    house_type = models.SmallIntegerField(
        'House type',
        choices=HouseType.choices,
        null=True,
        blank=True
    )

    room_type = models.SmallIntegerField(
        'Room type',
        choices=RoomType.choices,
        null=True,
        blank=True
    )

    unique_type = models.SmallIntegerField(
        'Unique type',
        choices=UniqueType.choices,
        null=True,
        blank=True
    )

    hotel_type = models.SmallIntegerField(
        'Hotel type',
        choices=HotelType.choices,
        null=True,
        blank=True
    )

    rent_type = models.SmallIntegerField(
        'Rent type',
        choices=RentType.choices,
        null=False,
        blank=False
    )

    guests_count = models.IntegerField(
        'Guests count',
        null=False,
        blank=False,
    )

    beds_count = models.IntegerField(
        'Beds count',
        null=False,
        blank=False,
    )

    bedrooms_count = models.IntegerField(
        'Bedrooms count',
        null=False,
        blank=False,
    )

    bathrooms_count = models.IntegerField(
        'Bathrooms count',
        null=False,
        blank=False,
    )

    price = models.DecimalField(
        'Price',
        max_digits=10,
        decimal_places=2,
        null=False,
        blank=False,
    )

    safety_deposit = models.DecimalField(
        'Safety deposit',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    description = models.TextField(
        'Description',
        null=True,
        blank=True,
    )

    is_available = models.BooleanField(
        'Available',
        default=True
    )

    rules = models.ForeignKey(
        'properties.Rules',
        on_delete=models.CASCADE,
        related_name="Properties",
    )

    additional_rules = models.TextField(
        'Additional rules',
        null=True,
        blank=True
    )

    unavailable_from = models.DateTimeField(
        'Unavailable from',
        null=True,
        blank=True
    )

    unavailable_to = models.DateTimeField(
        'Unavailable to',
        null=True,
        blank=True
    )

    arrival_time = models.TimeField(
        'Arrival time',
        null=False,
        blank=False
    )

    departure_time = models.TimeField(
        'Departure time',
        null=False,
        blank=False
    )

    status = models.SmallIntegerField(
        'Status',
        choices=Status.choices,
        null=False,
        blank=False,
        default=Status.PUBLISHED
    )

    views = models.IntegerField(
        'Views',
        default=0
    )

    created_at = models.DateTimeField(
        'Created at',
        auto_now_add=True,
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(
        'Updated at',
        auto_now=True,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Property {self.id}"

    @property
    def is_favorite(self):
        try:
            print(f"User {self.user}")
            print(f"Property {self.pk}")
            f = self.user.favorites.filter(object_id=self.pk).exists()
            print(f"Favorite {f}")
            return f
        except Exception as e:
            print(e)
            return False

    @property
    def favorites_count(self):
        count = Favorite.objects.filter(object_id=self.pk).count()
        return count

    @property
    def location(self) -> 'Location':
        from properties.serializers import LocationSerializer

        location = Location.objects.get(property=self)
        return LocationSerializer(location).data

    @property
    def images(self) -> list:
        images = LinkedImages.objects.filter(object_id=self.pk, content_type__model='properties')
        images_list = [image.image.url for image in images]
        return images_list

    @property
    def thumbnails(self) -> list:
        queryset = LinkedImages.objects.filter(object_id=self.pk, content_type__model='properties')
        thumbnail_list = []
        for thumbnail in queryset:
            if thumbnail.thumbnail:
                print(thumbnail.thumbnail)
                thumbnail_list.append(thumbnail.thumbnail.url)
        return thumbnail_list

    @property
    def amenities(self) -> list:
        amenities_queryset = AmenitiesBinding.objects.filter(property=self).values_list('amenity', flat=True)
        print(amenities_queryset)
        return amenities_queryset

    @property
    def rating_purity(self) -> int:
        purity = Review.objects.filter(content_type__model='properties', object_id=self.id).aggregate(
            models.Avg('purity'))
        return purity

    @property
    def rating_location(self) -> int:
        location = Review.objects.filter(content_type__model='properties', object_id=self.id).aggregate(
            models.Avg('location'))
        return location

    @property
    def rating_communication(self) -> int:
        communication = Review.objects.filter(content_type__model='properties', object_id=self.id).aggregate(
            models.Avg('communication'))
        return communication

    @property
    def rating_price_quality(self) -> int:
        price_quality = Review.objects.filter(content_type__model='properties', object_id=self.id).aggregate(
            models.Avg('price_quality'))
        return price_quality

    @property
    def rating_list(self) -> list:
        rating_list = []
        date_range = datetime.datetime.now() - datetime.timedelta(days=30), datetime.datetime.now()
        purity = Review.objects.filter(
            content_type__model='properties', object_id=self.id, created_at__range=date_range
        ).aggregate(models.Avg('purity'))['purity__avg']

        location = Review.objects.filter(
            content_type__model='properties', object_id=self.id, created_at__range=date_range
        ).aggregate(models.Avg('location'))['location__avg']

        communication = Review.objects.filter(
            content_type__model='properties', object_id=self.id, created_at__range=date_range
        ).aggregate(models.Avg('communication'))['communication__avg']

        price_quality = Review.objects.filter(
            content_type__model='properties', object_id=self.id, created_at__range=date_range
        ).aggregate(models.Avg('price_quality'))['price_quality__avg']
        if purity:
            if purity >= 4:
                rating_list.append({'purity': 'High'})
            elif purity >= 3:
                rating_list.append({'purity': 'Medium'})
            else:
                rating_list.append({'purity': 'Low'})

        if location:
            if location >= 4:
                rating_list.append({'location': 'High'})
            elif location >= 3:
                rating_list.append({'location': 'Medium'})
            else:
                rating_list.append({'location': 'Low'})

        if communication:
            if communication >= 4:
                rating_list.append({'communication': 'High'})
            elif communication >= 3:
                rating_list.append({'communication': 'Medium'})
            else:
                rating_list.append({'communication': 'Low'})

        if price_quality:
            if price_quality >= 4:
                rating_list.append({'price_quality': 'High'})
            elif price_quality >= 3:
                rating_list.append({'price_quality': 'Medium'})
            else:
                rating_list.append({'price_quality': 'Low'})
        print(rating_list)
        return rating_list

    @property
    def busy_time(self) -> list:
        busy_time = []
        orders_time = Orders.objects.filter(property=self).values_list('order_from', 'order_to')
        for time in orders_time:
            list_of_days_from_data_range(time[0], time[1], busy_time)
        busy_time.append(self.unavailable_from)
        busy_time.append(self.unavailable_to)
        busy_time = list(set(busy_time))
        return busy_time


class Rules(models.Model):

    children = models.BooleanField(
        'Children',
        default=True
    )

    suitable_for_babies = models.BooleanField(
        'Suitable for babies',
        default=True
    )

    pets = models.BooleanField(
        'Pets',
        default=True
    )

    smoking = models.BooleanField(
        'Smoking',
        default=True
    )

    parties = models.BooleanField(
        'Parties',
        default=True
    )

    def __str__(self):
        return f'Rules #{self.id}'


class AmenitiesBinding(models.Model):

    property = models.ForeignKey(
        'Properties',
        on_delete=models.CASCADE,
        related_name="AmenitiesBinding",
        null=True,
        blank=True
    )

    amenity = models.ForeignKey(
        'Amenities',
        on_delete=models.CASCADE,
        related_name="PropertiesBinding",
        null=True,
        blank=True,
    )

    custom_amenity = models.CharField(
        'Custom amenity',
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f'AmenitiesBinding #{self.id}'


class Amenities(models.Model):

    img = models.ImageField(
        'Image',
        upload_to=amenities_image_file_path,
        validators=[validate_images_file_max_size]
    )

    title = models.CharField(
        'Title',
        max_length=250,
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Amenity #{self.id}"


class Location(models.Model):

    property = models.ForeignKey(
        'Properties',
        on_delete=models.CASCADE,
        related_name="Location"
    )

    map_id = models.CharField(
        'Map_Id',
        max_length=80,
        null=True,
        blank=True,
    )

    country = models.CharField(
        'Country',
        max_length=40
    )

    city = models.CharField(
        'City',
        max_length=60
    )

    street = models.CharField(
        'Street',
        max_length=60,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"Location #{self.id}"


# TODO: delete later
class PropertyImages(models.Model):

    property = models.ForeignKey(
        'Properties',
        on_delete=models.CASCADE,
        related_name="property_images"
    )

    image = models.ImageField(
        verbose_name="Property image",
        upload_to=property_image_file_path,
        validators=[validate_images_file_max_size],
        null=True,
        blank=True
    )

    def __str__(self):
        return f"PropertyImages #{self.id}"
