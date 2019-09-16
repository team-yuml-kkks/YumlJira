import pytest

from .test_factories import ProjectFactory, TaskFactory


pytestmark = pytest.mark.django_db


def test_project_str():
    project = ProjectFactory()

    assert str(project) == project.name


def test_task_str():
    task = TaskFactory()

    assert str(task) == task.title

