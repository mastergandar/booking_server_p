from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.db.models import QuerySet
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from file_manager.models import LinkedImages
from social.models import Review, Notify, Report, Favorite, ReportMessages


class ReviewsSerializer(serializers.ModelSerializer):
    images_list = serializers.ListField(
        child=serializers.IntegerField(),
        required=False,
        allow_null=False,
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = Review
        fields = [
            'pk',
            'user',
            'content_type',
            'object_id',
            'images',
            'images_list',
            'description',
            'purity',
            'location',
            'communication',
            'price_quality',
        ]
        read_only_fields = [
            'pk',
            'object',
        ]

    def validate(self, attrs):
        attrs = super(ReviewsSerializer, self).validate(attrs)
        if 'images_list' in attrs:
            if attrs['images_list'] is None:
                raise ValidationError({'images_list': 'Images are required'})
            elif len(attrs['images_list']) < 3:
                raise ValidationError({'images_list': 'Images count must be greater than 2'})
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        images = validated_data.pop('images_list') if 'images_list' in validated_data else None

        review = Review.objects.create(**validated_data)

        for img_pk in images if images else []:
            ct = ContentType.objects.get_for_model(review.__class__)
            image = LinkedImages.objects.get(pk=img_pk)
            image.content_type = ct
            image.object_id = review.pk
            image.save()

        return review

    def to_representation(self, instance):

        from properties.serializers import SmallPropertiesSerializer
        from users.serializers import UserSerializer

        co_serializers = {
            'properties': SmallPropertiesSerializer,
            'user': UserSerializer
        }
        co_models = {
            'properties': apps.get_model('properties', 'Properties'),
            'user': apps.get_model('users', 'User')
        }

        rep = super(ReviewsSerializer, self).to_representation(instance)
        co_type = ContentType.objects.get(pk=rep['content_type']).name
        rep['user'] = co_serializers['user'](co_models['user'].objects.get(pk=rep['user'])).data
        rep['object'] = co_serializers[co_type](co_models[co_type].objects.get(pk=rep['object_id'])).data

        return rep


class ReportSerializers(serializers.ModelSerializer):
    images_list = serializers.ListField(
        child=serializers.IntegerField(),
        required=True,
        allow_null=False,
        allow_empty=False,
        write_only=True
    )

    class Meta:
        model = Report
        fields = [
            'pk',
            'user',
            'content_type',
            'object_id',
            'images',
            'images_list',
            'description',
            'report_type',
        ]
        read_only_fields = [
            'pk',
            'user',
            'object',
            'images',
        ]

    def validate(self, attrs):
        attrs = super(ReportSerializers, self).validate(attrs)
        if 'images_list' in attrs:
            if attrs['images_list'] is None:
                raise ValidationError({'images_list': 'Images are required'})
            elif len(attrs['images_list']) < 3:
                raise ValidationError({'images_list': 'Images count must be greater than 2'})
        attrs['user'] = self.context['request'].user
        return attrs

    def to_representation(self, instance):

        from properties.serializers import SmallPropertiesSerializer
        from users.serializers import UserSerializer

        co_serializers = {
            'properties': SmallPropertiesSerializer,
            'user': UserSerializer
        }
        co_models = {
            'properties': apps.get_model('properties', 'Properties'),
            'user': apps.get_model('users', 'User')
        }

        rep = super(ReportSerializers, self).to_representation(instance)
        co_type = ContentType.objects.get(pk=rep['content_type']).name
        rep['user'] = co_serializers['user'](co_models['user'].objects.get(pk=rep['user'])).data
        rep['object'] = co_serializers[co_type](co_models[co_type].objects.get(pk=rep['object_id'])).data

        return rep

    @transaction.atomic
    def create(self, validated_data):

        images = validated_data.pop('images_list', None)

        # co_type = ContentType.objects.get(pk=validated_data['content_type']).name}")
        co_model = apps.get_model('properties', validated_data['content_type'].name)
        co_obj = co_model.objects.get(pk=validated_data['object_id'])
        co_obj.is_available = False
        co_obj.save()
        report = super(ReportSerializers, self).create(validated_data)

        for img_pk in images:
            ct = ContentType.objects.get_for_model(report.__class__)
            image = LinkedImages.objects.get(pk=img_pk)
            image.content_type = ct
            image.object_id = report.pk
            image.save()

        return report


class NotifySerializer(serializers.ModelSerializer):
    class Meta:
        model = Notify
        fields = [
            'pk',
            'user',
            'code',
            'payload',
            'is_viewed',
            'created_at',
        ]


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorite
        fields = [
            'pk',
            'user',
            'content_type',
            'object_id',
            'created_at',
            'obj'
        ]
        read_only_fields = [
            'pk',
            'user',
            'obj'
        ]

    def validate(self, attrs):
        attrs = super(FavoriteSerializer, self).validate(attrs)
        attrs['user'] = self.context['request'].user
        return attrs

    def create(self, validated_data):
        try:
            instance = Favorite.objects.get(user=validated_data['user'], content_type=validated_data['content_type'],
                                            object_id=validated_data['object_id'])
            instance.delete()
            return Favorite.objects.none()
        except Favorite.DoesNotExist:
            instance = super(FavoriteSerializer, self).create(validated_data)
            # instance.obj = instance.content_type.model_class().objects.get(pk=instance.object_id)
            return instance

    def to_representation(self, instance):
        if type(instance) == QuerySet:
            return FavoriteSerializer(instance, many=True).data
        else:
            return super(FavoriteSerializer, self).to_representation(instance)


class ReportMessagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportMessages
        fields = [
            'pk',
            'report',
            'user',
            'message',
            'created_at',
        ]
        read_only_fields = [
            'pk',
            'user',
            'created_at',
        ]
