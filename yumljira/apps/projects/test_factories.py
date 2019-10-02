import factory
from factory import fuzzy
from factory.django import DjangoModelFactory as Factory
from faker import Faker

from yumljira.apps.users.test_factories import UserFactory

from .choices import *
from .models import *


class ProjectFactory(Factory):
    class Meta:
        model = Project

    name = factory.Faker('word')
    created_by = factory.SubFactory(UserFactory)
    key = factory.Faker('word')
    board_type = fuzzy.FuzzyChoice(BOARD_TYPE_KEYS)


class ColumnFactory(Factory):
    class Meta:
        model = Column

    project = factory.SubFactory(ProjectFactory)
    title = factory.Faker('word')
    number_in_board = factory.Faker('pyint')
    should_show = factory.Faker('pybool')


class TaskFactory(Factory):
    class Meta:
        model = Task

    title = factory.Faker('sentence')
    description = factory.Faker('sentence')

    project = factory.SubFactory(ProjectFactory)

    priority = fuzzy.FuzzyChoice(PRIORITIES_KEYS)

    created_by = factory.SubFactory(UserFactory)
    assigned_to = factory.SubFactory(UserFactory)

    task_type = fuzzy.FuzzyChoice(TASK_TYPES_KEYS)
    story = None

    column = factory.Faker('pyint')


class TimeLogFactory(Factory):
    class Meta:
        model = TimeLog

    task = factory.SubFactory(TaskFactory)
    user = factory.SubFactory(UserFactory)

    time_logged = factory.Faker('pyint')
    date = factory.Faker('date')


class CommentFactory(Factory):
    class Meta:
        model = Comment

    task = factory.SubFactory(TaskFactory)
    owner = factory.SubFactory(UserFactory)

    content = factory.Faker('paragraph')

