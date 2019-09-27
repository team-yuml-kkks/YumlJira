import pytest

from django.urls import reverse
from django.test import TestCase

from faker import Faker

from rest_framework import status
from rest_framework.test import APIClient

from yumljira.apps.common.test_utils import user_strategy

from .utils import add_token

from ..models import Comment
from ..serializers import CommentSerializer
from ..test_factories import CommentFactory

pytestmark = pytest.mark.django_db


class CommentViewsetTestCase(TestCase):
    def setUp(self):
        self.user, self.jwt = user_strategy()
        self.client = APIClient()
        self.url = reverse('comments-list')

    def test_create_comment(self):
        comment = CommentFactory()
        comments_before = Comment.objects.count()
        add_token(self.client, self.jwt)

        response = self.client.post(self.url, CommentSerializer(comment).data, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert comments_before + 1 == Comment.objects.count()

        assert response.data['owner'] == self.user.id
        assert response.data['content'] == comment.content
        assert response.data['task'] == comment.task.id

    def test_list_comment(self):
        comment = CommentFactory()
        add_token(self.client, self.jwt)

        response = self.client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1

        results = response.data['results']

        assert results[0]['pk'] == comment.pk

    def _detail_url(self, pk):
        return reverse('comments-detail', kwargs={'pk': pk})

    def test_put_comment(self):
        comment = CommentFactory(owner=self.user)
        add_token(self.client, self.jwt)

        content = Faker().word()
        data = CommentSerializer(comment).data
        data['content'] = content

        response = self.client.put(self._detail_url(comment.pk), data, format='json')

        assert response.status_code == status.HTTP_200_OK

        comment.refresh_from_db()

        assert comment.content == content

    def test_patch_comment(self):
        comment = CommentFactory(owner=self.user)
        add_token(self.client, self.jwt)

        content = Faker().word()

        response = self.client.patch(self._detail_url(comment.pk),
            {'content': content}, format='json')

        assert response.status_code == status.HTTP_200_OK

        comment.refresh_from_db()

        assert comment.content == content

    def test_delete_comment(self):
        comment = CommentFactory(owner=self.user)
        add_token(self.client, self.jwt)

        response = self.client.delete(self._detail_url(comment.pk))

        assert response.status_code == status.HTTP_204_NO_CONTENT

        try:
            comment.refresh_from_db()
            assert False
        except Comment.DoesNotExist:
            assert True

    def test_delete_comment_wrong_owner(self):
        comment = CommentFactory()
        add_token(self.client, self.jwt)

        response = self.client.delete(self._detail_url(comment.pk))

        assert response.status_code == status.HTTP_404_NOT_FOUND

        comment.refresh_from_db()

    def test_update_wrong_owner(self):
        comment = CommentFactory()
        add_token(self.client, self.jwt)
        data = CommentSerializer(comment).data

        response = self.client.put(self._detail_url(comment.pk), data, format='json')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_create_no_token(self):
        comment = CommentFactory()
        comments_before = Comment.objects.count()
        data = CommentSerializer(comment).data

        response = self.client.post(self.url, data, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert comments_before == Comment.objects.count()
