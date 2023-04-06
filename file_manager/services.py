
import tempfile
from datetime import datetime

from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils import timezone


def scale_image(
        image,
        quality: int = 80,
        width: int = None,
        height: int = None
) -> InMemoryUploadedFile:
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpeg')

    try:
        img = Image.open(image).convert('RGBA')
        size = [width, height]
        if (width and height) is None:
            size = img.size
        bg = Image.new('RGBA', img.size, (255, 255, 255))
        alpha_composite = Image.alpha_composite(bg, img)
        alpha_composite.thumbnail(size)
        alpha_composite = alpha_composite.convert('RGB')
        alpha_composite.save(tmp_file, format='JPEG', quality=quality)
    except IOError as e:
        tmp_file.close()
        raise RuntimeError(e)
    timestamp = str(datetime.timestamp(timezone.now())).split('.')[0]
    thumb_file = InMemoryUploadedFile(tmp_file, None, f'preview_{timestamp}.jpeg', 'image/jpeg', tmp_file.tell(), None)
    return thumb_file


def delete_old_files():
    from file_manager.models import LinkedImages
    old_un_attached_files = LinkedImages.objects.filter(
        object_id__isnull=True, updated_at__gt=timezone.now() - timezone.timedelta(days=30)
    )
    old_un_attached_files.delete()
