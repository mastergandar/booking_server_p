import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse

from properties.models import Properties


@pytest.mark.django_db
def test_upload_image(create_user_with_active_email, api_client_authed):
    ct = ContentType.objects.get_for_model(Properties)
    data = {
        'title': 'Test image',
        'image': open('test_files/img/test.jpeg', 'rb'),
        'content_type': ct.pk,
        'user': create_user_with_active_email().pk,
    }
    url = reverse('file_manager:image_list_create')
    response = api_client_authed.post(url, data=data, format='multipart')

    assert response.status_code == 201
