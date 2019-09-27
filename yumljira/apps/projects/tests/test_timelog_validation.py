import pytest
from string import ascii_lowercase

from django.urls import reverse
from django.test import TestCase

from faker import Faker

from hypothesis import given, settings
from hypothesis.extra.django import TestCase as HTestCase
from hypothesis.strategies import characters, integers, floats

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..choices import AVAILABLE_TIME_OPTIONS
from ..models import TimeLog
from ..serializers import TimeLogSerializer
from ..test_factories import TimeLogFactory

pytestmark = pytest.mark.django_db


class TimeLogTimeLoggedValidationTestCase(HTestCase):
    NOT_AVAILABLE = [x for x in ascii_lowercase if x not in AVAILABLE_TIME_OPTIONS]

    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.api_client = APIClient()
        self.url = reverse('timelogs-list')
        add_token(self.api_client, self.jwt)

    @given(characters(
        whitelist_categories=['Ll'],
        min_codepoint=97,
        max_codepoint=122,
        blacklist_characters=NOT_AVAILABLE
    ), integers(min_value=1, max_value=200))
    @settings(max_examples=15)
    def test_time_logged_correct_w_integer(self, character, number):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = f'{number}{character}'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    @given(characters(
        whitelist_categories=['Ll'],
        min_codepoint=97,
        max_codepoint=122,
        blacklist_characters=NOT_AVAILABLE
    ), floats(min_value=1, max_value=200))
    @settings(max_examples=15)
    def test_time_logged_correct_w_float(self, character, number):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = f'{number}{character}'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    @given(characters(
        whitelist_categories=['Ll'],
        blacklist_characters=AVAILABLE_TIME_OPTIONS
    ))
    def test_time_logged_wrong_str(self, character):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = character

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @given(characters(
        whitelist_categories=['Ll'],
        blacklist_characters=AVAILABLE_TIME_OPTIONS
    ), integers())
    @settings(max_examples=30)
    def test_time_logged_wrong_option(self, character, number):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = f'{number}{character}'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @given(characters(
        whitelist_categories=['Ll'],
        blacklist_characters=AVAILABLE_TIME_OPTIONS
    ))
    def test_time_logged_only_one_wrong_option(self, character):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = f'15m 2h 1{character}'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_time_logged_good_options_wrong_str(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '2h15m'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_time_logged_negative_str_start(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '-1h'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_time_logged_negative_str(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '1h -30m'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_time_logged_0(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '0m'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    @given(characters(
        whitelist_categories=['Lu'],
        whitelist_characters=('M', 'H', 'D', 'W')
    ), integers())
    @settings(max_examples=30)
    def test_time_logged_upper_case(self, character, number):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = f'{number}{character}'

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST


class LogTimeCalculationsTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.api_client = APIClient()
        self.url = reverse('timelogs-list')
        add_token(self.api_client, self.jwt)

    def test_time_logged_minute(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '30m'

        response = self.api_client.post(self.url, data, format='json')

        assert response.data['time_logged'] == '30'

    def test_time_logged_hour(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '1h'

        response = self.api_client.post(self.url, data, format='json')

        assert response.data['time_logged'] == '60'

    def test_time_logged_hour_minute(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '1h 30m'

        response = self.api_client.post(self.url, data, format='json')

        assert response.data['time_logged'] == '90'

        data['time_logged'] = '30m 1h'

        response = self.api_client.post(self.url, data, format='json')

        assert response.data['time_logged'] == '90'

    def test_time_logged_float_hour(self):
        log = TimeLogFactory()
        data = TimeLogSerializer(log).data
        data['time_logged'] = '0.5h'

        response = self.api_client.post(self.url, data, format='json')

        assert response.data['time_logged'] == '30.0'
