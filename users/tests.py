import pytest

from django.urls import reverse

from users.models import User


@pytest.mark.django_db
def test_unauthorized_request(api_client):
    url = reverse('users:me')
    response = api_client.get(url)
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_create():
    User.objects.create_user(username='user', email='user@mail.com', password='password')
    assert User.objects.count() == 1


@pytest.mark.django_db
def test_user_detail(client, create_user):
    user = create_user(username='someone')
    url = reverse('users:user_view', kwargs={'pk': user.pk})
    response = client.get(url)
    assert response.status_code == 200
    assert 'someone' in response.data['username']


@pytest.mark.django_db
def test_user_register(client, rand_test_password):
    url = reverse('users:register')
    data = {
        'username': 'register',
        'password': rand_test_password,
        'email': 'test@booking.com',
    }
    response = client.post(url, data=data)

    assert response.status_code == 201

    assert 'register' in response.data['username']
    assert 'test@booking.com' in response.data['email']


@pytest.mark.django_db
def test_user_activate(client, create_user):
    user = create_user(username='test', email='test@mail.com', password='password')
    assert User.objects.get(pk=user.pk).is_email_active is False

    code = User.objects.get(pk=user.pk).activation_email_code
    url = reverse('users:activate_account', kwargs={'uid': user.pk, 'token': code})

    response = client.get(url)

    assert response.status_code == 200
    assert response.data['message'] == 'Account activated successfully'
    assert User.objects.get(pk=user.pk).is_email_active is True
    assert User.objects.get(pk=user.pk).activation_email_code is None


"""@pytest.mark.django_db
def test_auth_view(auto_login_user):
    client, user = auto_login_user()
    url = reverse('users:me')
    response = client.get(url)
    assert response.status_code == 200"""


@pytest.mark.django_db
def test_authorized_request(api_client, get_or_create_token):
    url = reverse('users:me')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_update_user(api_client, get_or_create_token):
    data = {
        'phone_number': '89114508507',
        'bio': 'test bio update'
    }
    url = reverse('users:me')
    api_client.credentials(HTTP_AUTHORIZATION='Bearer %s' % get_or_create_token.access_token)
    response = api_client.patch(url, data=data)
    assert response.status_code == 200
    assert '89114508507' in response.data['phone_number']
    assert 'test bio update' in response.data['bio']
