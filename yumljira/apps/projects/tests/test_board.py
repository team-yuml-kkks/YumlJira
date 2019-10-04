import pytest

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from faker import Faker

from hypothesis import given, settings
from hypothesis.extra.django import TestCase as HTestCase
from hypothesis.strategies import integers

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..choices import KANBAN, SCRUM, SELECTED_FOR_DEV, TO_DO
from ..models import Column, Project
from ..serializers import ProjectSerializer, TaskSerializer
from ..test_factories import ColumnFactory, ProjectFactory, TaskFactory


pytestmark = pytest.mark.django_db


def test_column_unique_together():
    project = ProjectFactory()
    column = ColumnFactory(project=project, number_in_board=1)

    try:
        column2 = ColumnFactory(project=project, number_in_board=1)
        assert False
    except IntegrityError:
        assert True


class KanbanBoardTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.api_client = APIClient()
        self.url = reverse('projects-list')

    def test_create_kanban_project_with_sprint_name(self):
        project = ProjectFactory(board_type=KANBAN)
        projects_before = Project.objects.count()

        data = ProjectSerializer(project).data
        data['sprint_name'] = Faker().word()

        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert projects_before == Project.objects.count()

    def test_create_kanban_project(self):
        project = ProjectFactory(board_type=KANBAN)
        projects_before = Project.objects.count()

        data = ProjectSerializer(project).data

        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert projects_before + 1 == Project.objects.count()

        project = Project.objects.last()

        assert project.columns.count() == 4

        second_column_title = project.columns \
            .filter(number_in_board=2) \
            .first() \
            .title

        assert second_column_title == SELECTED_FOR_DEV


class ScrumBoardTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.api_client = APIClient()
        self.url = reverse('projects-list')

    def test_create_scrum_no_sprint_name(self):
        project = ProjectFactory(board_type=SCRUM)
        projects_before = Project.objects.count()

        data = ProjectSerializer(project).data

        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert projects_before == Project.objects.count()

    def test_create_scrum_with_sprint_name(self):
        project = ProjectFactory(board_type=SCRUM)
        projects_before = Project.objects.count()

        data = ProjectSerializer(project).data
        data['sprint_name'] = Faker().word()

        add_token(self.api_client, self.jwt)

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert projects_before + 1 == Project.objects.count()

        project = Project.objects.last()

        assert project.columns.count() == 4

        second_column_title = project.columns \
            .filter(number_in_board=2) \
            .first() \
            .title

        assert second_column_title == TO_DO


class ColumnValidationTestCase(HTestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.tasks_url = reverse('tasks-list')
        self.projects_url = reverse('projects-list')

        self.api_client = APIClient()
        add_token(self.api_client, self.jwt)

        project = ProjectFactory(board_type=KANBAN)
        data = ProjectSerializer(project).data
        response = self.api_client.post(self.projects_url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

        self.project = Project.objects.last()

    @given(integers(min_value=1, max_value=4))
    def test_column_exist(self, number):
        column = self.project.columns.filter(number_in_board=number).first()
        task = TaskFactory(column=column)
        data = TaskSerializer(task).data

        response = self.api_client.post(self.tasks_url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED

    def test_column_not_exist(self):
        task = TaskFactory()
        data = TaskSerializer(task).data
        data['column'] = task.column.pk + 1

        response = self.api_client.post(self.tasks_url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def _detail_url(self, pk):
        return reverse('tasks-detail', kwargs={'pk': pk})

    @given(integers(min_value=1, max_value=4))
    def test_update_task_column_exist(self, number):
        column = self.project.columns.filter(number_in_board=number).first()
        task = TaskFactory(column=column)

        response = self.api_client.patch(self._detail_url(task.pk),
            {'column': column.pk}, format='json')

        assert response.status_code == status.HTTP_200_OK

        task.refresh_from_db()

        assert task.column.pk == column.pk

    def test_update_task_column_not_exist(self):
        task = TaskFactory()
        column_pk = task.column.pk + 1

        response = self.api_client.patch(self._detail_url(task.pk),
            {'column': column_pk}, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST

        task.refresh_from_db()

        assert task.column.pk is not column_pk

