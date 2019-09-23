import json
import pytest

from django.urls import reverse
from django.test import TestCase

from faker import Faker

from hypothesis import given, settings
from hypothesis.extra.django import TestCase as HTestCase
from hypothesis.strategies import integers

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .models import *
from .serializers import TaskSerializer, TimeLogSerializer
from .test_factories import ProjectFactory, TaskFactory, TimeLogFactory


pytestmark = pytest.mark.django_db


def test_project_str():
    project = ProjectFactory()

    assert str(project) == project.name


def test_task_str():
    task = TaskFactory()

    assert str(task) == task.title


def project_json(project):
    return {
        'name': project.name,
    }


def add_token(client, jwt):
    client.credentials(HTTP_AUTHORIZATION='JWT ' + jwt)


class ProjectTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.client = APIClient()
        self.url = reverse('projects-list')

    def test_create_project(self):
        project = ProjectFactory()
        projects_before = Project.objects.count()
        add_token(self.client, self.jwt)

        response = self.client.post(self.url, project_json(project), format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert projects_before + 1 == Project.objects.count()

        assert response.data['name'] == project.name
        assert response.data['created_by'] == self.user.id

    def test_list_projects(self):
        project = ProjectFactory(created_by=self.user)
        project2 = ProjectFactory(created_by=self.user)

        add_token(self.client, self.jwt)

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

        data = response.data['results']

        assert 'name' in data[0]
        assert 'tasks' in data[0]
        assert 'created_by' in data[0]

        assert data[0]['name'] == project.name
        assert data[0]['created_by'] == self.user.id

    def test_no_credentials(self):
        project = ProjectFactory()
        project2 = ProjectFactory()

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.post(self.url, project_json(project), format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_project_create_no_data(self):
        projects_before = Project.objects.count()
        add_token(self.client, self.jwt)

        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert projects_before == Project.objects.count()

    # TODO: ADD TESTS FOR UPDATE


class TaskTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.client = APIClient()
        self.url = reverse('tasks-list')

    def test_create_task(self):
        project = ProjectFactory()
        task = TaskFactory(project=project)
        tasks_before = Task.objects.count()
        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert tasks_before + 1 == Task.objects.count()

        assert response.data['title'] == task.title
        assert response.data['priority'] == task.priority
        assert response.data['created_by'] == self.user.id
        assert response.data['project'] == project.id

    def test_list_tasks(self):
        project = ProjectFactory()
        task = TaskFactory(created_by=self.user, project=project)
        task2 = TaskFactory(created_by=self.user)
        add_token(self.client, self.jwt)

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 2

        data = response.data['results']

        assert 'description' in data[0]
        assert 'created_by' in data[0]
        assert 'priority' in data[0]
        assert 'assigned_to' in data[0]
        assert 'project' in data[0]

        assert data[0]['title'] == task.title
        assert data[0]['created_by'] == self.user.id
        assert data[0]['project'] == project.id

    def test_no_credentials(self):
        task = TaskFactory()
        task2 = TaskFactory()

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_task_create_no_data(self):
        tasks_before = Task.objects.count()
        add_token(self.client, self.jwt)

        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    def test_task_create_with_story(self):
        project = ProjectFactory()

        task_story = TaskFactory(project=project, task_type=STORY)
        task = TaskFactory(project=project, task_type=SUBTASK, story=task_story)
        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_task_create_with_story_wrong_type(self):
        project = ProjectFactory()

        task_story = TaskFactory(project=project, task_type=SUBTASK)
        task = TaskFactory(project=project, task_type=SUBTASK, story=task_story)

        tasks_before = Task.objects.count()

        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    def test_task_story_to_story(self):
        project = ProjectFactory()

        task_story = TaskFactory(project=project, task_type=STORY)
        task = TaskFactory(project=project, task_type=STORY, story=task_story)

        tasks_before = Task.objects.count()

        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    # TODO: ADD TESTS FOR UPDATE

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
        # task.refresh_from_db()

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
