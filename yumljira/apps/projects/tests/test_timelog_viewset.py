import pytest
from urllib import parse

from django.urls import reverse

from faker import Faker

from hypothesis import given, settings
from hypothesis.extra.django import TestCase as HTestCase
from hypothesis.strategies import integers

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..models import Task, TimeLog
from ..serializers import TaskSerializer, TimeLogSerializer
from ..test_factories import ProjectFactory, TaskFactory, TimeLogFactory

pytestmark = pytest.mark.django_db


class TimeLogViewsetTestCase(HTestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.api_client = APIClient()
        self.url = reverse('timelogs-list')

    def test_create_time_log(self):
        log = TimeLogFactory(user=self.user)
        logs_before = TimeLog.objects.count()

        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, TimeLogSerializer(log).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert logs_before + 1 == TimeLog.objects.count()

    def test_create_time_log_no_credentials(self):
        log = TimeLogFactory()
        logs_before = TimeLog.objects.count()

        response = self.api_client.post(self.url, TimeLogSerializer(log).data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert logs_before == TimeLog.objects.count()

    def _details_url(self, pk):
        return reverse('timelogs-detail', kwargs={'pk': pk})

    def test_delete_time_log(self):
        log = TimeLogFactory(user=self.user)
        logs_before = TimeLog.objects.count()

        add_token(self.api_client, self.jwt)

        response = self.api_client.delete(self._details_url(log.id))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert logs_before - 1 == TimeLog.objects.count()

    def test_detele_task_do_not_delete_time_log(self):
        task = TaskFactory(created_by=self.user)
        log = TimeLogFactory(task=task, user=self.user)

        add_token(self.api_client, self.jwt)

        logs_before = TimeLog.objects.count()

        response = self.api_client.delete(reverse('tasks-detail', kwargs={'pk': task.pk}))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        log.refresh_from_db()

        try:
            task.refresh_from_db()
            assert False
        except Task.DoesNotExist:
            assert True

        assert logs_before == TimeLog.objects.count()
        assert not log.task

    def test_user_cannot_delete_not_owned_logs(self):
        log = TimeLogFactory()
        logs_before = TimeLog.objects.count()

        add_token(self.api_client, self.jwt)

        response = self.api_client.delete(self._details_url(log.id))

        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert logs_before == TimeLog.objects.count()

    @given(integers(min_value=1, max_value=200), integers(min_value=1, max_value=200))
    @settings(max_examples=10)
    def test_user_cannot_update_not_owned_logs(self, time_before, time_update):
        log = TimeLogFactory(time_logged=time_before)
        add_token(self.api_client, self.jwt)

        response = self.api_client.patch(self._details_url(log.id), {'time_logged': time_update}, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

        log.refresh_from_db()
        assert log.time_logged == time_before

    @given(integers(min_value=1, max_value=200), integers(min_value=1, max_value=200))
    @settings(max_examples=10)
    def test_user_can_patch_owned_logs(self, time_before, time_update):
        log = TimeLogFactory(time_logged=time_before, user=self.user)
        add_token(self.api_client, self.jwt)

        response = self.api_client.patch(self._details_url(log.id), {'time_logged': time_update}, format='json')

        assert response.status_code == status.HTTP_200_OK

        log.refresh_from_db()
        assert log.time_logged == time_update

    def test_user_cannot_log_0_minutes(self):
        log = TimeLogFactory(time_logged=0)
        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, TimeLogSerializer(log).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_time_logged_no_task(self):
        log = TimeLogFactory(task=None)
        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, TimeLogSerializer(log).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_time_log_list_filter(self):
        project = ProjectFactory()
        task = TaskFactory(project=project)
        task2 = TaskFactory()
        log = TimeLogFactory(task=task, date='2019-09-24')
        log2 = TimeLogFactory(date='2019-09-17')

        add_token(self.api_client, self.jwt)

        response = self.api_client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

        query = parse.urlencode({'task': task.pk})

        response = self.api_client.get(f'{self.url}?{query}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['pk'] == log.pk

        query = parse.urlencode({'task__project': task.project.pk})
        response = self.api_client.get(f'{self.url}?{query}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['pk'] == log.pk

        query = parse.urlencode({'date_after': '2019-09-18'})
        response = self.api_client.get(f'{self.url}?{query}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['pk'] == log.pk

        query = parse.urlencode({'date_before': '2019-09-23'})
        response = self.api_client.get(f'{self.url}?{query}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['pk'] == log2.pk

        query = parse.urlencode({'date_after': '2019-09-18', 'date_before': '2019-09-23'})
        response = self.api_client.get(f'{self.url}?{query}')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 0


@given(integers(min_value=1, max_value=200), integers(min_value=1, max_value=200))
@settings(max_examples=10)
def test_task_serializer_time_logged(time1, time2):
    task = TaskFactory()
    log = TimeLogFactory(task=task, time_logged=time1)
    log2 = TimeLogFactory(task=task, time_logged=time2)

    data = TaskSerializer(task).data

    assert data['time_logged'] == time1 + time2


def test_task_no_time_logged():
    data = TaskSerializer(TaskFactory()).data

    assert data['time_logged'] == 0
