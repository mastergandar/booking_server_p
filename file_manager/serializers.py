from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from file_manager.models import LinkedImages


class LinkedImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = LinkedImages
        fields = [
            'pk',
            'user',
            'title',
            'content_type',
            'object_id',
            'image',
            'thumbnail',
        ]
        read_only_fields = [
            'pk',
            'content_object',
            'thumbnail',
        ]

    def validate(self, attrs):
        attrs = super(LinkedImagesSerializer, self).validate(attrs)
        attrs['user'] = self.context['request'].user
        try:
            images_count = LinkedImages.objects.filter(
                content_type=attrs['content_type'],
                object_id=attrs['object_id'],
                user=self.context['request'].user
            ).count()
        except KeyError:
            images_count = 0
        if self.context['request'].method == 'PATCH':
            linked_image = LinkedImages.objects.get(pk=attrs['pk'])
            if linked_image.user != self.context['request'].user:
                raise ValidationError('You can not edit this image')
        if attrs['content_type'] == 'properties' and images_count >= 30:
            raise ValidationError(f'You can not upload more than 30 images for this property')
        elif attrs['content_type'] == ('review' or 'report') and images_count >= 10:
            raise ValidationError(f'You can not upload more than 10 images for {attrs["content_type"]}')
        return attrs

    def to_representation(self, instance):
        ret = super(LinkedImagesSerializer, self).to_representation(instance)
        return ret
