import json

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.apps import apps

from file_manager.models import LinkedImages
from properties.tests import cre_prop
from social.enums import ReportType
from social.models import Review


def cre_fav(create_user_with_active_email, object_id, content_type):
    user = create_user_with_active_email()
    model = apps.get_model('social', 'Favorite')
    return model.objects.create(
        user=user,
        object_id=object_id,
        content_type=content_type
    )


@pytest.fixture
def create_random_review_to_property(create_user_with_active_email, create_random_property):
    ct = ContentType.objects.get_for_model(apps.get_model('properties', 'Properties'))
    kwargs = {
        'user': create_user_with_active_email(),
        'description': 'Test random review creation',
        'content_type': ct,
        'object_id': create_random_property.pk,
    }
    review = Review.objects.create(**kwargs)
    return review


@pytest.mark.django_db
def test_review_to_property_creation(api_client, create_user_with_active_email,
                                     create_random_property, get_or_create_token):
    user = create_user_with_active_email()
    property = create_random_property
    ct = ContentType.objects.get_for_model(apps.get_model('properties', 'Properties'))
    images = []
    for i in range(0, 3):
        images.append(LinkedImages.objects.create(
            title='Test image',
            content_type=ct,
            object_id=None,
            image='./test_files/img/test.jpg',
            user=user,
        ).pk)
    data = {
        'user': user.pk,
        'description': 'Test random review creation',
        'content_type': ct.pk,
        'object_id': property.pk,
        'images_list': images,
    }
    url = reverse('social_booking:review_create')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    print(data)
    response = api_client.post(url, data=data)
    print(response.data)
    assert response.status_code == 201
    assert ct.pk == response.data['content_type']
    assert user.pk == response.data['user']['pk']


@pytest.mark.django_db
def test_report_to_property_creation(api_client, create_user_with_active_email,
                                     create_random_property, get_or_create_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    user = api_client.get(reverse('users:me'), format='json').data
    property = create_random_property
    ct = ContentType.objects.get_for_model(apps.get_model('properties', 'Properties'))
    images = []
    for i in range(0, 3):
        images.append(LinkedImages.objects.create(
            title='Test image',
            content_type=ct,
            object_id=None,
            image='./test_files/img/test.jpg',
            user=create_user_with_active_email(),
        ).pk)
    data = {
        'description': 'Test random review creation',
        'content_type': ct.pk,
        'object_id': property.pk,
        'images_list': images,
        'report_type': ReportType.INCORRECT_DATA.value,
    }
    url = reverse('social_booking:report_create')
    print(data)
    response = api_client.post(url, data=data)
    print(response.data)
    assert response.status_code == 201
    assert ct.pk == response.data['content_type']
    assert user['pk'] == response.data['user']['pk']


@pytest.mark.django_db
def test_review_to_property_list(api_client, get_or_create_token, create_random_review_to_property):
    review = create_random_review_to_property
    url = reverse('social_booking:review_list', kwargs={'content_type': 'properties'})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == 200


"""@pytest.mark.django_db
def test_review_to_property_update(api_client, get_or_create_token, create_random_review_to_property):
    data = {
        'title': 'Test review updated',
    }
    review = create_random_review_to_property
    url = reverse('social_booking:review_retrieve_update', kwargs={'pk': create_random_review_to_property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    print(response.data)
    assert response.status_code == 200
    assert 'Test review updated' in response.data['title']"""


@pytest.mark.django_db
def test_favorite_create(api_client, create_user_with_active_email,
                         create_random_property, get_or_create_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    property = create_random_property
    url = reverse('social_booking:favorite_list_create')
    data = {
        'content_type': ContentType.objects.get_for_model(apps.get_model('properties', 'Properties')).pk,
        'object_id': property.pk,
    }

    response = api_client.post(url, data=data)

    assert response.status_code == 201
    assert property.pk == response.data['object_id']


@pytest.mark.django_db
def test_favorite_list(create_user_with_active_email, api_client, get_or_create_token):
    favorite_list = []
    property_list = [cre_prop(create_user_with_active_email) for i in range(0, 3)]
    ct = ContentType.objects.get_for_model(apps.get_model('properties', 'Properties'))
    for i in range(0, 3):
        favorite_list.append(cre_fav(create_user_with_active_email, property_list[i].pk, ct))
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    url = reverse('social_booking:favorite_list_create')
    response = api_client.get(url)
    print(response.data)
    print(favorite_list)
    assert response.status_code == 200
    assert len(response.data) == 3


@pytest.mark.django_db
def test_favorite_delete(api_client, create_user_with_active_email, create_random_property, get_or_create_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    property = create_random_property
    ct = ContentType.objects.get_for_model(apps.get_model('properties', 'Properties'))
    favorite = cre_fav(create_user_with_active_email, property.pk, ct)
    url = reverse('social_booking:favorite_retrieve_destroy', kwargs={'pk': favorite.pk})
    response = api_client.delete(url)
    print(response.data)
    assert response.status_code == 204


@pytest.mark.django_db
def test_favorite_get(api_client, create_user_with_active_email, create_random_property, get_or_create_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    property = create_random_property
    ct = ContentType.objects.get_for_model(apps.get_model('properties', 'Properties'))
    favorite = cre_fav(create_user_with_active_email, property.pk, ct)
    url = reverse('social_booking:favorite_retrieve_destroy', kwargs={'pk': favorite.pk})
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == 200
