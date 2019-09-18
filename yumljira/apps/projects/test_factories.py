import factory
from factory import fuzzy
from factory.django import DjangoModelFactory as Factory
from faker import Faker

from yumljira.apps.users.test_factories import UserFactory

from .choices import *
from .models import Project, Task


class ProjectFactory(Factory):
    class Meta:
        model = Project

    name = factory.Faker('word')
    created_by = factory.SubFactory(UserFactory)


class TaskFactory(Factory):
    class Meta:
        model = Task

    title = factory.Faker('sentence')
    description = factory.Faker('sentence')

    project = factory.SubFactory(ProjectFactory)

    priority = fuzzy.FuzzyChoice(PRIORITIES_KEYS)

    created_by = factory.SubFactory(UserFactory)
    assigned_to = factory.SubFactory(UserFactory)

