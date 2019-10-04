import pytest

from django.urls import reverse
from django.test import TestCase

from faker import Faker

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..choices import KANBAN, STORY, SUBTASK
from ..models import Project, Task
from ..serializers import ProjectSerializer, TaskSerializer
from ..test_factories import ProjectFactory, TaskFactory

pytestmark = pytest.mark.django_db


class TaskTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.client = APIClient()
        self.url = reverse('tasks-list')

        project_client = APIClient()
        add_token(project_client, self.jwt)

        project = ProjectFactory(board_type=KANBAN)
        data = ProjectSerializer(project).data
        response = project_client.post(reverse('projects-list'), data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        self.project = Project.objects.last()

    def test_create_task(self):
        task = TaskFactory()
        tasks_before = Task.objects.count()
        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert tasks_before + 1 == Task.objects.count()

        assert response.data['title'] == task.title
        assert response.data['priority'] == task.priority
        assert response.data['created_by'] == self.user.id

    def test_list_tasks(self):
        task = TaskFactory(created_by=self.user)
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
        assert 'column' in data[0]

        assert data[0]['title'] == task.title
        assert data[0]['created_by'] == self.user.id

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
        column = self.project.columns.first()
        task_story = TaskFactory(task_type=STORY, column=column)
        task = TaskFactory(task_type=SUBTASK, story=task_story, column=column)
        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_task_create_with_story_wrong_type(self):
        column = self.project.columns.first()
        task_story = TaskFactory(task_type=SUBTASK, column=column)
        task = TaskFactory(task_type=SUBTASK, story=task_story, column=column)

        tasks_before = Task.objects.count()

        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    def test_task_story_to_story(self):
        column = self.project.columns.first()
        task_story = TaskFactory(task_type=STORY, column=column)
        task = TaskFactory(task_type=STORY, story=task_story, column=column)

        tasks_before = Task.objects.count()

        add_token(self.client, self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    def _detail_url(self, pk):
        return reverse('tasks-detail', kwargs={'pk': pk})

    def test_task_delete(self):
        task = TaskFactory()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        response = self.client.delete(self._detail_url(task.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_task_update_patch(self):
        task = TaskFactory()
        title = Faker().word()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.patch(self._detail_url(task.pk), {'title': title}, format='json')

        assert response.status_code == status.HTTP_200_OK

        task.refresh_from_db()

        assert task.title == title

    def test_task_update_put(self):
        task = TaskFactory()
        title = Faker().word()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        data = TaskSerializer(task).data
        data['title'] = title

        response = self.client.put(self._detail_url(task.pk), data, format='json')

        assert response.status_code == status.HTTP_200_OK

        task.refresh_from_db()

        assert task.title == title
