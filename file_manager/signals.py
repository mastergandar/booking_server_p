from django.db.models.signals import post_save
from django.dispatch import receiver

from file_manager.services import scale_image


@receiver(post_save, sender='file_manager.LinkedImages')
def create_thumbnail_on_img_upload(sender, instance, update_fields, **kwargs):
    if update_fields:
        for field in iter(update_fields):
            if field == 'image':
                if instance.image:
                    thumb = scale_image(instance.image)
                    instance.thumbnail.save(thumb.name, thumb, save=True)
