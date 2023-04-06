from hashlib import md5


def get_storage_path_static(key, filename, directory):
    return f"{directory}/{key}/{filename}"


def get_filename_by_hash(file, filename) -> str:
    file.seek(0)
    file_hash = md5(file.read()).hexdigest()
    return f"{file_hash}.{filename.split('.')[-1]}"


def avatar_property_avatar_path(instance, filename):
    return get_storage_path_static(
        instance.pk,
        get_filename_by_hash(instance.avatar, filename),
        'avatars'
    )


def amenities_image_file_path(instance, filename):
    return f'amenities_images/{get_filename_by_hash(instance.image, filename)}'


def property_image_file_path(instance, filename):
    return f'property_images/{get_filename_by_hash(instance.image, filename)}'


def review_image_file_path(instance, filename):
    return f'review_images/{get_filename_by_hash(instance.image, filename)}'


def report_image_file_path(instance, filename):
    return f'report_images/{get_filename_by_hash(instance.image, filename)}'


def dynamic_image_file_path(instance, filename):
    from properties.models import Properties
    from social.models import Report, Review
    try:
        return f'dynamic_images/{instance.get_object().__name__}/{get_filename_by_hash(instance.image, filename)}'
    except (AttributeError, Properties.DoesNotExist, Report.DoesNotExist, Review.DoesNotExist):
        return f'dynamic_images/{instance.content_type.name}/{get_filename_by_hash(instance.image, filename)}'
