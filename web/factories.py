import factory

from web.models import User


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda instance: f"{instance.username}@addefan.dev")
    password = factory.Faker("password")

    class Meta:
        model = User
