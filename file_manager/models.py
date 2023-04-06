from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from core.file_storage import dynamic_image_file_path
from core.validators import validate_images_file_max_size


class LinkedImages(models.Model):
    limit = models.Q(app_label='properties', model='properties') | \
            models.Q(app_label='social', model='review') | \
            models.Q(app_label='social', model='report')

    title = models.CharField(max_length=100)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, limit_choices_to=limit)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name="LinkedImages"
    )

    image = models.ImageField(
        verbose_name="Linked image",
        upload_to=dynamic_image_file_path,
        validators=[validate_images_file_max_size],
        null=True,
        blank=True,
    )

    thumbnail = models.ImageField(
        verbose_name="Linked image thumbnail",
        upload_to=dynamic_image_file_path,
        validators=[validate_images_file_max_size],
        null=True,
        blank=True,
    )

    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def save(self, *args, **kwargs):
        if self.__class__ == LinkedImages:
            try:
                cls = self.__class__
                old = cls.objects.get(pk=self.pk)
                new = self
                changed_fields = []
                for field in cls._meta.get_fields():
                    field_name = field.name
                    try:
                        if getattr(old, field_name) != getattr(new, field_name):
                            changed_fields.append(field_name)
                    except Exception as ex:
                        pass
                kwargs['update_fields'] = changed_fields
            except LinkedImages.DoesNotExist:
                pass
            print(f"LinkedImages.save() kwargs: {kwargs}")
            if 'update_fields' in kwargs and 'content_object' in kwargs['update_fields']:
                kwargs['update_fields'].remove('content_object')
            super().save(*args, **kwargs)
        else:
            pass

    def get_object(self):
        return self.content_type.get_object_for_this_type(pk=self.object_id)
