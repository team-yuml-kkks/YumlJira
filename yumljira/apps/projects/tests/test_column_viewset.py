import pytest

from django.urls import reverse

from hypothesis import given, settings
from hypothesis.extra.django import TestCase
from hypothesis.strategies import builds, characters, integers, text

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..models import Column
from ..serializers import ColumnSerializer, ProjectSerializer
from ..test_factories import ColumnFactory, ProjectFactory


class ColumnViewsTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.api_client = APIClient()
        self.url = reverse('columns-list')

        self.project = ProjectFactory()
        self.project.create_kanban_board()

        add_token(self.api_client, self.jwt)

    def _detail_url(self, pk):
        return reverse('columns-detail', kwargs={'pk': pk})

    @given(
        builds(ColumnFactory.build,
            number_in_board=integers(min_value=5, max_value=5),
            title=text(min_size=1, max_size=20,
                alphabet=characters(whitelist_categories=('Ll', 'Lu'))))
    )
    def test_create_new_column(self, column):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        columns_before = Column.objects.count()
        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert columns_before + 1 == Column.objects.count()

        assert response.data['title'] == data['title']
        assert response.data['should_show']
        assert response.data['removable']

    @given(
        builds(ColumnFactory.build,
            number_in_board=integers(min_value=5, max_value=200))
    )
    def test_create_new_column_no_project(self, column):
        data = ColumnSerializer(column).data
        columns_before = Column.objects.count()

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert columns_before == Column.objects.count()

    @given(
        builds(ColumnFactory.build, number_in_board=integers(min_value=1, max_value=4))
    )
    def test_update_column_put(self, column):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        response = self.api_client.post(self.url, data, format='json')

        response = self.api_client.put(self._detail_url(response.data['pk']),
            data, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == data['title']

    @given(
        builds(ColumnFactory.build, number_in_board=integers(min_value=1, max_value=4)),
        text(min_size=1, max_size=20, alphabet=characters(whitelist_categories=('Ll', 'Lu')))
    )
    def test_update_column_patch(self, column, new_title):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        response = self.api_client.post(self.url, data, format='json')

        response = self.api_client.patch(self._detail_url(response.data['pk']),
            {'title': new_title}, format='json')

        assert response.status_code == status.HTTP_200_OK
        assert response.data['title'] == new_title

    @given(
        builds(ColumnFactory.build, number_in_board=integers(min_value=5, max_value=5))
    )
    def test_remove_column(self, column):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        response = self.api_client.post(self.url, data, format='json')
        response = self.api_client.delete(self._detail_url(response.data['pk']))

        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_remove_column_not_removable(self):
        column = self.project.columns.first()
        response = self.api_client.delete(self._detail_url(column.pk))

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @given(
        builds(ColumnFactory.build, number_in_board=integers(min_value=1, max_value=4))
    )
    def test_create_correct_number(self, column):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert self.project.columns.count() == 5

        new_column = self.project.columns.filter(number_in_board=data['number_in_board']).first()

        assert new_column.title == data['title']

    @given(
        builds(ColumnFactory.build, number_in_board=integers(min_value=6, max_value=100))
    )
    def test_create_incorrect_number(self, column):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.project.columns.count() == 4

    def test_create_0(self):
        column = ColumnFactory(number_in_board=0)
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        response = self.api_client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.project.columns.count() == 4

    @given(
        builds(ColumnFactory.build, number_in_board=integers(min_value=1, max_value=4))
    )
    def test_remove_column(self, column):
        data = ColumnSerializer(column).data
        data['project'] = self.project.pk

        pk = self.api_client.post(self.url, data, format='json').data['pk']
        response = self.api_client.delete(self._detail_url(pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert self.project.columns.count() == 4

        assert not self.project.columns.filter(pk=pk).first()

    @given(
        integers(min_value=1, max_value=4),
        integers(min_value=5, max_value=100)
    )
    def test_patch_column_wrong_number(self, old_number, number):
        column = self.project.columns.filter(number_in_board=old_number).first()

        response = self.api_client.patch(self._detail_url(column.pk),
            {'number_in_board': number}, format='json')

        print(response.data)
        print(self.project.columns.all().values_list('number_in_board'))

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert self.project.columns.count() == 4

