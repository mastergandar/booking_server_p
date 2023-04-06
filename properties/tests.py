import datetime
import random

import pytest
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils import timezone
from rest_framework.exceptions import ErrorDetail

from file_manager.models import LinkedImages
from properties.enums import RentType, AccommodationType, HotelType, UniqueType, RoomType, HouseType, FlatType, Status
from properties.models import Amenities, AmenitiesBinding, Rules, Properties, Location


@pytest.mark.django_db
def test_get_properties_list(api_client_authed):
    url = reverse('properties:properties_list')
    response = api_client_authed.get(url)

    assert response.status_code == 200


def cre_prop(create_user_with_active_email):
    kwargs = {
        'user': create_user_with_active_email(),
        'title': 'Test property',
        'is_available': True,
        'rules': Rules.objects.create(),
        'arrival_time': '12:00',
        'departure_time': '12:00',
    }

    accommodation_type = AccommodationType.FLAT.value

    kwargs['accommodation_type'] = accommodation_type

    kwargs['flat_type'] = FlatType.ATELIER.value

    kwargs['guests_count'] = random.randint(1, 10)
    kwargs['beds_count'] = random.randint(1, 10)
    kwargs['bedrooms_count'] = random.randint(1, 10)
    kwargs['bathrooms_count'] = random.randint(1, 10)

    kwargs['rent_type'] = random.choice(list(RentType))

    kwargs['price'] = random.randint(1, 1000)

    kwargs['description'] = 'Test description'

    obj = Properties.objects.create(**kwargs)
    print(obj.price)
    Location.objects.create(country='Test country', city='Test city', street='Test street', property=obj)
    return obj


def cre_prop_user_obj(user_with_active_email):
    kwargs = {
        'user': user_with_active_email,
        'title': 'Test property',
        'is_available': True,
        'rules': Rules.objects.create(),
        'arrival_time': '12:00',
        'departure_time': '12:00',
    }

    accommodation_type = AccommodationType.FLAT.value

    kwargs['accommodation_type'] = accommodation_type

    kwargs['flat_type'] = FlatType.ATELIER.value

    kwargs['guests_count'] = random.randint(1, 10)
    kwargs['beds_count'] = random.randint(1, 10)
    kwargs['bedrooms_count'] = random.randint(1, 10)
    kwargs['bathrooms_count'] = random.randint(1, 10)

    kwargs['rent_type'] = random.choice(list(RentType))

    kwargs['price'] = random.randint(1, 1000)

    kwargs['description'] = 'Test description'

    obj = Properties.objects.create(**kwargs)
    print(obj.price)
    Location.objects.create(country='Test country', city='Test city', street='Test street', property=obj)
    return obj


@pytest.mark.django_db
def test_create_property(create_user_with_active_email, api_client_authed):
    user = create_user_with_active_email()
    data = {
        'user': user.pk,
        'title': 'Test property',
        'is_available': True,
        'rules_list': [True, False, True, False, True],
        'arrival_time': '12:00',
        'departure_time': '12:00',
    }

    accommodation_type = random.choice(list(AccommodationType))

    data['accommodation_type'] = accommodation_type.value

    if accommodation_type == AccommodationType.FLAT:
        data['flat_type'] = random.choice(list(FlatType))
    elif accommodation_type == AccommodationType.HOUSE:
        data['house_type'] = random.choice(list(HouseType))
    elif accommodation_type == AccommodationType.ROOM:
        data['room_type'] = random.choice(list(RoomType))
    elif accommodation_type == AccommodationType.UNIQUE:
        data['unique_type'] = random.choice(list(UniqueType))
    elif accommodation_type == AccommodationType.HOTEL:
        data['hotel_type'] = random.choice(list(HotelType))

    data['guests_count'] = random.randint(1, 10)
    data['beds_count'] = random.randint(1, 10)
    data['bedrooms_count'] = random.randint(1, 10)
    data['bathrooms_count'] = random.randint(1, 10)

    data['rent_type'] = random.choice(list(RentType))

    data['price'] = random.randint(1, 1000)

    data['description'] = 'Test description'

    ct = ContentType.objects.get_for_model(Properties)

    images = []
    for i in range(0, 3):
        images.append(LinkedImages.objects.create(
            title='Test image',
            content_type=ct,
            object_id=None,
            image='./test_files/img/test.jpg',
            user=user,
        ).pk)

    data['images_list'] = images

    amenities = []
    for i in range(0, 2):
        amenities.append(Amenities.objects.create(
            img=f'./media/amenities_images/1{i}.png', title=f'Test amenities_{i}').pk,
        )

    data['amenities_list'] = list(set(amenities))

    data['rules'] = Rules.objects.create().pk
    data['location_data'] = ['Russia', 'Moscow', 'Angels Lane']

    url = reverse('properties:my_properties_list_create')
    response = api_client_authed.post(url, data=data)
    # print(LinkedImages.objects.all().first().content_object)
    print(response.data)
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_property(api_client, get_or_create_token, create_random_property):
    data = {
        'title': 'Update title',
    }
    property = create_random_property
    url = reverse('properties:property_retrieve_update_delete', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    assert response.status_code == 200
    assert 'Update title' in response.data['title']


@pytest.mark.django_db
def test_update_guests_error_property(api_client, get_or_create_token, create_random_property):
    data = {
        'guests_count': 0,
    }
    property = create_random_property
    url = reverse('properties:property_retrieve_update_delete', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_accommodation_error_property(api_client, get_or_create_token, create_random_property):
    data = {
        'accommodation_type': 0,
        'flat_type': 1,
    }
    property = create_random_property
    url = reverse('properties:property_retrieve_update_delete', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    print(response.data)
    assert response.status_code == 400
    assert response.data['house_type'] == [ErrorDetail(string='This field is required', code='invalid')]


@pytest.mark.django_db
def test_update_beds_error_property(api_client, get_or_create_token, create_random_property):
    data = {
        'beds_count': -1,
    }
    property = create_random_property
    url = reverse('properties:property_retrieve_update_delete', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    print(response.data)
    assert response.status_code == 400
    assert response.data['beds_count'] == [ErrorDetail(string='Beds count must be positive', code='invalid')]


@pytest.mark.django_db
def test_update_bedrooms_error_property(api_client, get_or_create_token, create_random_property):
    data = {
        'bedrooms_count': -1,
    }
    property = create_random_property
    url = reverse('properties:property_retrieve_update_delete', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    print(response.data)
    assert response.status_code == 400
    assert response.data['bedrooms_count'] == [ErrorDetail(string='Bedrooms count must be positive', code='invalid')]


@pytest.mark.django_db
def test_update_bathrooms_error_property(api_client, get_or_create_token, create_random_property):
    data = {
        'bathrooms_count': -1,
    }
    property = create_random_property
    url = reverse('properties:property_retrieve_update_delete', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    print(response.data)
    assert response.status_code == 400
    assert response.data['bathrooms_count'] == [ErrorDetail(string='Bathrooms count must be positive', code='invalid')]


@pytest.mark.django_db
def test_order_property(api_client, get_or_create_token, create_random_property):
    now = timezone.now()
    tomorrow = now + datetime.timedelta(days=1)
    data = {
        'order_from': now,
        'order_to': tomorrow,
    }
    property = create_random_property
    url = reverse('properties:property_order', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.post(url, data=data)
    print(response.data)
    assert response.status_code == 201
    assert now.strftime('%Y-%m-%dT%H:%M:%S.%f') == response.data['order_from']
    assert tomorrow.strftime('%Y-%m-%dT%H:%M:%S.%f') == response.data['order_to']


@pytest.mark.django_db
def test_recommendation_property(api_client, create_user_with_active_email, get_or_create_token, create_flat_property):
    cre_prop(create_user_with_active_email)
    cre_prop(create_user_with_active_email)
    property = create_flat_property
    url = reverse('properties:properties_recommendation', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.get(url)
    print(response.data)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_property_move_to_archive(api_client, create_user_with_active_email, create_random_property):
    from users.tokens.serializers import TokenObtainPairSerializer

    user = create_user_with_active_email()
    token = TokenObtainPairSerializer.get_token(user)
    property = cre_prop_user_obj(user)
    url = reverse('properties:property_archive', kwargs={'pk': property.pk})
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % token.access_token)
    response = api_client.post(url)
    print(response.data)
    assert response.status_code == 200
    assert response.data['status'] == Status.ARCHIVED.value
