import pytest

from django.urls import reverse
from django.test import TestCase

from faker import Faker

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..models import Project
from ..serializers import ProjectSerializer
from ..test_factories import ProjectFactory


pytestmark = pytest.mark.django_db


def test_project_str():
    project = ProjectFactory()

    assert str(project) == project.name

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

    def _detail_url(self, pk):
        return reverse('projects-detail', kwargs={'pk': pk})

    def test_project_delete(self):
        project = ProjectFactory()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)
        response = self.client.delete(self._detail_url(project.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_project_update_patch(self):
        project = ProjectFactory()
        name = Faker().word()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        response = self.client.patch(self._detail_url(project.pk), {'name': name}, format='json')

        assert response.status_code == status.HTTP_200_OK

        project.refresh_from_db()

        assert project.name == name

    def test_project_update_put(self):
        project = ProjectFactory()
        name = Faker().word()

        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + self.jwt)

        data = ProjectSerializer(project).data
        data['name'] = name

        response = self.client.put(self._detail_url(project.pk), data, format='json')

        assert response.status_code == status.HTTP_200_OK

        project.refresh_from_db()

        assert project.name == name
