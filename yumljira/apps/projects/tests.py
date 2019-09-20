import json
import pytest

from django.urls import reverse
from django.test import TestCase

from faker import Faker

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .models import *
from .serializers import TaskSerializer
from .test_factories import ProjectFactory, TaskFactory


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


class ProjectTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.client = APIClient()
        self.url = reverse('projects-list')

    def test_create_project(self):
        project = ProjectFactory()
        projects_before = Project.objects.count()
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.post(self.url, project_json(project), format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert projects_before + 1 == Project.objects.count()

        assert response.data['name'] == project.name
        assert response.data['created_by'] == self.user.id

    def test_list_projects(self):
        project = ProjectFactory(created_by=self.user)
        project2 = ProjectFactory(created_by=self.user)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

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
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

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
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

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

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

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
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.post(self.url)

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    def test_task_create_with_story(self):
        project = ProjectFactory()

        task_story = TaskFactory(project=project, task_type=STORY)
        task = TaskFactory(project=project, task_type=SUBTASK, story=task_story)

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_task_create_with_story_wrong_type(self):
        project = ProjectFactory()

        task_story = TaskFactory(project=project, task_type=SUBTASK)
        task = TaskFactory(project=project, task_type=SUBTASK, story=task_story)

        tasks_before = Task.objects.count()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    def test_task_story_to_story(self):
        project = ProjectFactory()

        task_story = TaskFactory(project=project, task_type=STORY)
        task = TaskFactory(project=project, task_type=STORY, story=task_story)

        tasks_before = Task.objects.count()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.post(self.url, TaskSerializer(task).data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert tasks_before == Task.objects.count()

    # TODO: ADD TESTS FOR UPDATE

