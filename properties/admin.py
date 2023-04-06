from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from django.utils.safestring import mark_safe

from file_manager.models import LinkedImages
from properties.models import Properties, AmenitiesBinding, Location, Rules, Amenities


class PropertyImageInline(GenericTabularInline):
    model = LinkedImages
    extra = 0
    readonly_fields = ["rendered_image", "rendered_thumbnail"]
    fields = ["title", "image", "rendered_image", "rendered_thumbnail", "user"]

    def rendered_image(self, obj):
        if obj.image:
            url = obj.image.storage.url(name=obj.image.name)
            return mark_safe(
                f"""<img src="{url}" width=320 height=240 />"""
            )
        return ""

    def rendered_thumbnail(self, obj):
        if obj.thumbnail:
            url = obj.thumbnail.storage.url(name=obj.thumbnail.name)
            return mark_safe(
                f"""<img src="{url}" width=320 height=240 />"""
            )
        return ""


class PropertyLoactionInline(admin.StackedInline):
    model = Location
    extra = 0


class PropertyAmenityInline(admin.StackedInline):
    model = AmenitiesBinding
    extra = 0


@admin.register(Properties)
class PropertiesAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'user',
        'title',
        'views',
        'favorites_count',
        'accommodation_type',
        'flat_type',
        'house_type',
        'room_type',
        'unique_type',
        'hotel_type',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'user',
                'title',
                'status',
                'views',
                'favorites_count',
                ]
        }),
        ('ACCOMMODATION', {
            "fields": [
                'accommodation_type',
                'flat_type',
                'house_type',
                'room_type',
                'unique_type',
                'hotel_type',
                ]
        }),
        ('RENT', {
            "fields": [
                'guests_count',
                'beds_count',
                'bedrooms_count',
                'bathrooms_count',
                'rent_type',
                'price',
                'safety_deposit',
                'is_available',
                'arrival_time',
                'departure_time',
                ]
        }),
        ('DESCRIPTION', {
            "fields": [
                'description',
                'rules',
                'additional_rules',
            ]
        }),
    )
    inlines = [
        PropertyImageInline,
        PropertyLoactionInline,
        PropertyAmenityInline,
    ]
    readonly_fields = ['favorites_count', 'views']


@admin.register(Rules)
class RulesAdmin(admin.ModelAdmin):
    list_display = [
        'pk',
        'children',
        'suitable_for_babies',
        'pets',
        'smoking',
        'parties',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'children',
                'suitable_for_babies',
                'pets',
                'smoking',
                'parties',
            ]
        }),
    )


@admin.register(Amenities)
class Amenities(admin.ModelAdmin):
    list_display = [
        'pk',
        'rendered_image',
        'title',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'title',
                'img',
                'rendered_image',
            ]
        }),
    )

    readonly_fields = ["rendered_image"]

    def rendered_image(self, obj):
        if obj.img:
            url = obj.img.storage.url(name=obj.img.name)
            return mark_safe(
                f"""<img src="{url}" width=320 height=240 />"""
            )
        return ""


@admin.register(AmenitiesBinding)
class AmenitiesBinding(admin.ModelAdmin):
    list_display = [
        'pk',
        'property',
        'amenity',
        'custom_amenity',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'property',
                'amenity',
                'custom_amenity',
            ]
        }),
    )


@admin.register(Location)
class Location(admin.ModelAdmin):
    list_display = [
        'pk',
        'property',
        'country',
        'city',
        'street',
        'map_id',
    ]
    fieldsets = (
        ('MAIN', {
            "fields": [
                'property',
                'country',
                'city',
                'street',
                'map_id',
            ]
        }),
    )
