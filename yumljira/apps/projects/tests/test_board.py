import pytest

from django.db.utils import IntegrityError
from django.test import TestCase
from django.urls import reverse

from faker import Faker

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..choices import KANBAN, SCRUM, SELECTED_FOR_DEV, TO_DO
from ..models import Project
from ..serializers import ProjectSerializer
from ..test_factories import ColumnFactory, ProjectFactory


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

