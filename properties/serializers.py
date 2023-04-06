from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from file_manager.models import LinkedImages
from properties.models import Properties, Rules, AmenitiesBinding, Amenities, Location
from properties.service import PropertyService


class PropertiesSerializer(serializers.ModelSerializer):
    images_list = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_null=False,
        allow_empty=False,
        write_only=True
    )

    amenities_list = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=True,
        allow_empty=True,
        write_only=True,
    )

    location_data = serializers.ListField(
        child=serializers.CharField(),
        required=True,
        allow_null=False,
        allow_empty=False,
        write_only=True
    )

    rules_list = serializers.ListField(
        child=serializers.BooleanField(),
        required=True,
        allow_null=False,
        allow_empty=False,
        write_only=True,
    )

    class Meta:
        model = Properties
        fields = [
            'pk',
            'user',
            'title',
            'accommodation_type',
            'flat_type',
            'house_type',
            'room_type',
            'unique_type',
            'hotel_type',
            'guests_count',
            'rent_type',
            'beds_count',
            'bedrooms_count',
            'bathrooms_count',
            'price',
            'safety_deposit',
            'description',
            'is_available',
            'arrival_time',
            'departure_time',
            'rules',
            'rules_list',
            'additional_rules',
            'location',
            'location_data',
            'images',
            'images_list',
            'amenities',
            'amenities_list',
            'rating_purity',
            'rating_location',
            'rating_communication',
            'rating_price_quality',
            'rating_list',
            'status',
            'views',
            'is_favorite',
        ]
        read_only_fields = [
            'pk',
            'user',
            'location',
            'rules',
            'images',
            'amenities'
            'rating_purity',
            'rating_location',
            'rating_communication',
            'rating_price_quality',
            'rating_list',
            'status',
            'views',
            'is_favorite',
        ]

    def validate(self, attrs):
        attrs = super().validate(attrs)
        if self.context['request'].method == 'POST':

            PropertyService.property_type_validation(attrs)

            if attrs['guests_count'] is None:
                raise ValidationError({'guests_count': 'This field is required.'})
            elif attrs['guests_count'] < 1:
                raise ValidationError({'guests_count': 'This field must be greater than 0.'})

            if attrs['beds_count'] is None:
                raise ValidationError({'beds_count': 'This field is required.'})

            if attrs['bedrooms_count'] is None:
                raise ValidationError({'bedrooms_count': 'This field is required.'})

            if attrs['bathrooms_count'] is None:
                raise ValidationError({'bathrooms_count': 'This field is required.'})

            if attrs['price'] is None:
                raise ValidationError({'price': 'This field is required.'})
            elif attrs['price'] < 0:
                raise ValidationError({'price': 'Price must be greater than 0'})

            if attrs['images_list'] is None:
                raise ValidationError({'images_list': 'Images list is required'})
            elif len(attrs['images_list']) < 3:
                raise ValidationError({'images_list': 'Images count must be greater than 2'})

            if attrs['title'] is None:
                raise ValidationError({'title': 'Title is required'})

            if attrs['rent_type'] is None:
                raise ValidationError({'rent_type': 'Rent type is required'})

            if 'rules_list' in attrs:
                if attrs['rules_list'] is None:
                    raise ValidationError({'rules_list': 'Rules list is required'})
                rules_fields = ['children', 'suitable_for_babies', 'pets', 'smoking', 'parties']
                attrs['rules_list'] = {x: y for x in rules_fields for y in attrs['rules_list']}
            attrs['location_data'] = {
                'country': attrs['location_data'][0],
                'city': attrs['location_data'][1],
                'street': attrs['location_data'][2]
            }

        elif self.context['request'].method == 'PATCH':
            if 'accommodation_type' in attrs:

                PropertyService.property_type_validation(attrs)

            if 'guests_count' in attrs:
                if attrs['guests_count'] is None:
                    raise ValidationError({'guests_count': 'Guests count is required'})
                elif attrs['guests_count'] < 1:
                    raise ValidationError({'guests_count': 'Guests count must be greater than 0'})

            if 'beds_count' in attrs:
                if attrs['beds_count'] is None:
                    raise ValidationError({'beds_count': 'Beds count is required'})
                elif attrs['beds_count'] < 0:
                    raise ValidationError({'beds_count': 'Beds count must be positive'})

            if 'bedrooms_count' in attrs:
                if attrs['bedrooms_count'] is None:
                    raise ValidationError({'bedrooms_count': 'Bedrooms count is required'})
                elif attrs['bedrooms_count'] < 0:
                    raise ValidationError({'bedrooms_count': 'Bedrooms count must be positive'})

            if 'bathrooms_count' in attrs:
                if attrs['bathrooms_count'] is None:
                    raise ValidationError({'bathrooms_count': 'Bathrooms count is required'})
                elif attrs['bathrooms_count'] < 0:
                    raise ValidationError({'bathrooms_count': 'Bathrooms count must be positive'})

            if 'price' in attrs:
                if attrs['price'] is None:
                    raise ValidationError({'price': 'Price is required'})
                elif attrs['price'] < 0:
                    raise ValidationError({'price': 'Price must be greater than 0'})

            if 'images_list' in attrs:
                if attrs['images_list'] is None:
                    raise ValidationError({'images_list': 'Images are required'})
                elif len(attrs['images_list']) < 3:
                    raise ValidationError({'images_list': 'Images count must be greater than 2'})

            if 'title' in attrs:
                if attrs['title'] is None:
                    raise ValidationError({'title': 'Title is required'})

            if 'rent_type' in attrs:
                if attrs['rent_type'] is None:
                    raise ValidationError({'rent_type': 'Rent type is required'})

            if 'rules_list' in attrs:
                if attrs['rules_list'] is None:
                    pass
                else:
                    rules_fields = ['children', 'suitable_for_babies', 'pets', 'smoking', 'parties']
                    attrs['rules_list'] = {x: y for x in rules_fields for y in attrs['rules_list']}

            if 'arrival_time' not in attrs:
                pass

            if 'departure_time' not in attrs:
                pass

            if 'location_data' in attrs:
                attrs['location_data'] = {
                    'country': attrs['location_data'][0],
                    'city': attrs['location_data'][1],
                    'street': attrs['location_data'][2]
                }
            else:
                pass

        if 'safety_deposit' not in attrs:
            attrs['safety_deposit'] = 0
        attrs['user'] = self.context['request'].user
        return attrs

    @transaction.atomic
    def update(self, instance, validated_data):
        if 'images_list' in validated_data:
            images_list = validated_data.pop('images_list')
            validated_data['arrival_time'] = instance.arrival_time
            validated_data['departure_time'] = instance.departure_time
            ct = ContentType.objects.get_for_model(instance.__class__)
            for image_id in images_list:
                if not LinkedImages.objects.filter(pk=image_id).exists():
                    image = LinkedImages.objects.get(pk=image_id)
                    image.content_type = ct
                    image.object_id = instance.pk
                    image.save()
                elif not LinkedImages.objects.filter(pk=image_id, content_type=ct, object_id=instance.pk).exists():
                    LinkedImages.objects.get(pk=image_id).update(content_type=ct, object_id=instance.pk)

        if 'rules_list' in validated_data:
            rules_list = validated_data.pop('rules_list')
            if instance.rules is None:
                rule = Rules(**rules_list)
                rule.save()
                validated_data['rules'] = rule
            else:
                instance.rules.update(**rules_list)

        if 'amenities_list' in validated_data:
            amenities_list = validated_data.pop('amenities_list')

            AmenitiesBinding.objects.filter(property=instance).delete()
            for amenity_id in amenities_list:
                AmenitiesBinding.objects.create(
                    property=instance,
                    amenity_id=amenity_id
                )
            if 23 in amenities_list or 24 in amenities_list:
                try:
                    rule.children = True
                    rule.save()
                except Exception as e:
                    instance.rules.update(children=True)

        if 'location_data' in validated_data:
            instance.location.country = validated_data['location_data']['country']
            instance.location.city = validated_data['location_data']['city']
            instance.location.street = validated_data['location_data']['street']
            instance.location.save()

        instance = super().update(instance, validated_data)

        return instance

    @transaction.atomic
    def create(self, validated_data):
        images = validated_data.pop('images_list')
        location = validated_data.pop('location_data')
        amenities = None
        if 'amenities_list' in validated_data:
            amenities = validated_data.pop('amenities_list')
        rules_list = validated_data.pop('rules_list')
        rule = Rules(**rules_list)
        rule.save()
        validated_data['rules'] = rule

        property = Properties.objects.create(**validated_data)
        print(f"Property: {property}")
        for img_pk in images:
            ct = ContentType.objects.get_for_model(property.__class__)
            image = LinkedImages.objects.get(pk=img_pk)
            image.content_type = ct
            image.object_id = property.pk
            image.save()

        if amenities:
            for amenity_pk in amenities:
                AmenitiesBinding.objects.create(property=property, amenity=Amenities.objects.get(pk=amenity_pk))
            if 23 in amenities or 24 in amenities:
                rule.children = True
                rule.save()

        Location.objects.create(**location, property=property)

        return property

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['amenities'] = instance.amenities
        return rep


class SmallPropertiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Properties
        fields = [
            'pk',
            'user',
            'title',
            'is_available',
            'location',
            'price',
            'rating_purity',
            'rating_location',
            'rating_communication',
            'rating_price_quality',
            'rating_list',
            'images',
            'amenities',
            'views',
            'is_favorite',
        ]
        read_only_fields = [
            'pk',
            'user',
            'title',
            'is_available',
            'location',
            'price',
            'rating_purity',
            'rating_location',
            'rating_communication',
            'rating_price_quality',
            'rating_list',
            'images',
            'views',
            'is_favorite',
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['images'] = instance.thumbnails
        return rep


class PropertiesPromotionSerializer(SmallPropertiesSerializer):

    class Meta:
        model = Properties
        fields = [
            *SmallPropertiesSerializer.Meta.fields,
        ]
        read_only_fields = [
            *SmallPropertiesSerializer.Meta.read_only_fields,
        ]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        from payments.models import PromotionObjects
        if PromotionObjects.objects.filter(content_type=ContentType.objects.get_for_model(instance.__class__),
                                           object_id=instance.pk).exists():
            rep['is_promoted'] = True
        else:
            rep['is_promoted'] = False
        return rep


class RulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rules
        fields = [
            'pk',
            'children',
            'suitable_for_babies',
            'pets',
            'smoking',
            'parties',
        ]
        read_only_fields = [
            'pk',
        ]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = [
            'pk',
            'country',
            'city',
            'street',
            'property',
        ]
        read_only_fields = [
            'pk',
            'property',
        ]


class AmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Amenities
        fields = [
            'pk',
            'title',
            'img',
        ]
        read_only_fields = [
            'pk',
            'title',
            'img',
        ]
