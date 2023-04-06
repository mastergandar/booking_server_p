import pytest
import random
import uuid

from django.contrib.contenttypes.models import ContentType

from properties.enums import RentType, AccommodationType, FlatType, HouseType, RoomType, UniqueType, HotelType
from properties.models import Properties, Rules, Location
from social.models import Favorite
from users.tokens.serializers import TokenObtainPairSerializer


@pytest.fixture
def rand_test_password():
    return 'test_pass' + str(random.randint(1, 100))


@pytest.fixture
def create_user(db, django_user_model, rand_test_password):
    def make_user(**kwargs):
        kwargs['password'] = rand_test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4()) + '@' + str(uuid.uuid4()) + '.com'
        return django_user_model.objects.create_user(**kwargs)
    return make_user


@pytest.fixture
def create_user_with_active_email(db, django_user_model, rand_test_password):
    def make_user(**kwargs):
        kwargs['password'] = rand_test_password
        if 'username' not in kwargs:
            kwargs['username'] = str(uuid.uuid4())
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4()) + '@' + str(uuid.uuid4()) + '.com'
        kwargs['is_email_active'] = True
        return django_user_model.objects.create_user(**kwargs)
    return make_user


"""@pytest.fixture
def auto_login_user(db, client, create_user, rand_test_password):
    def make_auto_login(user=None):
        if user is None:
            user = create_user()
        client.login(username=user.username, password=rand_test_password)
        return client, user
    return make_auto_login"""


@pytest.fixture
def get_or_create_token(db, create_user_with_active_email):
    user = create_user_with_active_email()
    token = TokenObtainPairSerializer.get_token(user)
    return token


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def api_client_authed(api_client, get_or_create_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    return api_client


@pytest.fixture
def create_random_property(create_user_with_active_email):

    kwargs = {
        'user': create_user_with_active_email(),
        'title': 'Test property',
        'is_available': True,
        'rules': Rules.objects.create(),
        'arrival_time': '12:00',
        'departure_time': '12:00',
        }

    accommodation_type = random.choice(list(AccommodationType))

    kwargs['accommodation_type'] = accommodation_type.value

    if accommodation_type == AccommodationType.FLAT:
        kwargs['flat_type'] = random.choice(list(FlatType))
    elif accommodation_type == AccommodationType.HOUSE:
        kwargs['house_type'] = random.choice(list(HouseType))
    elif accommodation_type == AccommodationType.ROOM:
        kwargs['room_type'] = random.choice(list(RoomType))
    elif accommodation_type == AccommodationType.UNIQUE:
        kwargs['unique_type'] = random.choice(list(UniqueType))
    elif accommodation_type == AccommodationType.HOTEL:
        kwargs['hotel_type'] = random.choice(list(HotelType))

    kwargs['guests_count'] = random.randint(1, 10)
    kwargs['beds_count'] = random.randint(1, 10)
    kwargs['bedrooms_count'] = random.randint(1, 10)
    kwargs['bathrooms_count'] = random.randint(1, 10)

    kwargs['rent_type'] = random.choice(list(RentType))

    kwargs['price'] = random.randint(1, 1000)

    kwargs['description'] = 'Test description'

    obj = Properties.objects.create(**kwargs)

    Location.objects.create(country='Test country', city='Test city', street='Test street', property=obj)

    return obj


@pytest.fixture
def create_flat_property(create_user_with_active_email):

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

    Location.objects.create(country='Test country', city='Test city', street='Test street', property=obj)

    return obj


@pytest.fixture
def create_favorite_property(create_user_with_active_email, create_random_property):
    user = create_user_with_active_email()
    property = create_random_property
    favorite = Favorite.objects.create(
        user=user, content_type=ContentType.objects.get_for_model(property), object_id=property.id
    )
    return favorite
