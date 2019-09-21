from django.conf import settings
from django.core.files.base import File
from django.urls import reverse

from faker import Faker

import pytest

from rest_framework import status
from rest_framework.test import APIClient

from .test_factories import UserFactory
from .utils import get_image_file


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

