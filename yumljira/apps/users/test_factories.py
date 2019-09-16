from django.contrib.auth import get_user_model

import factory
from factory import fuzzy
from factory.django import DjangoModelFactory as Factory
from faker import Faker


class UserFactory(Factory):
    class Meta:
        model = get_user_model()

    email = factory.Faker('email')
    username = factory.Faker('pystr')

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
