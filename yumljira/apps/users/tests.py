from allauth.socialaccount.models import SocialAccount

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.base import File
from django.test import TestCase
from django.urls import reverse

from faker import Faker

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from .test_factories import UserFactory
from .utils import get_image_file
from .views import GoogleLoginView


pytestmark = pytest.mark.django_db


def test_get_avatar_when_no_avatar_file():
    user = UserFactory(avatar=None)
    avatar_url = settings.DEFAULT_AVATAR.split('.')[0]

    assert '/static/{}'.format(avatar_url) in user.get_avatar


def test_get_avatar_with_file():
    user = UserFactory()

    assert user.get_avatar == '/uploads/{}'.format(user.avatar.name)


def test_get_image():
    file = get_image_file()

    assert isinstance(file, File)
    assert file.name == 'test.png'


def test_register_user_no_image():
    client = APIClient()
    url = reverse('rest_register')

    password = Faker().pystr(min_chars=8)

    data = {
        'email': Faker().email(),
        'password1': password,
        'password2': password,
        'username': Faker().user_name(),
    }

    response = client.post(url, data, format='json')

    assert response.status_code == status.HTTP_201_CREATED


def test_register_user_with_image():
    client = APIClient()
    url = reverse('rest_register')

    password = Faker().pystr(min_chars=8)

    data = {
        'email': Faker().email(),
        'password1': password,
        'password2': password,
        'username': Faker().user_name(),
        'avatar': get_image_file()
    }

    response = client.post(url, data, format='multipart')

    assert response.status_code == status.HTTP_201_CREATED


class GoogleLoginTests(TestCase):

    def _mock_google_response(self, **options):
        data = {
            "family_name": Faker().last_name(),
            "email": Faker().email(),
            "given_name": Faker().first_name(),
            "sub": Faker().isbn10()
        }

        data.update(**options)

        return data

    def test_google_login_create_user(self):
        users_before = get_user_model().objects.count()

        data = self._mock_google_response()
        user, _ = GoogleLoginView().create_user(data)

        assert user
        assert users_before + 1 == get_user_model().objects.count()

        assert user.username == data['email']
        assert user.first_name == data['given_name']
        assert user.email == data['email']

        social_acc = SocialAccount.objects.last()

        assert social_acc.user == user

    def test_google_login_create_user_exists(self):
        data = self._mock_google_response()
        user = UserFactory(email=data['email'], username=data['email'])

        user2, _ = GoogleLoginView().create_user(data)

        user.refresh_from_db()

        assert user2
        assert user2 == user

    def test_google_login_response(self):
        user = UserFactory()

        response = GoogleLoginView().get_response_data(user)

        assert response.status_code == status.HTTP_201_CREATED
        assert 'token' in response.data
        assert 'user' in response.data

    def test_google_view_no_token(self):
        users_before = get_user_model().objects.count()
        client = APIClient()

        response = client.post(reverse('google-login'))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert users_before == get_user_model().objects.count()

