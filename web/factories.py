import factory

from web.models import User, Link, Visit
from django.utils.timezone import now

from web.services import generate_short_link


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    username = factory.Faker("user_name")
    email = factory.LazyAttribute(lambda instance: f"{instance.username}@addefan.dev")
    password = factory.Faker("password")

    class Meta:
        model = User


class LinkFactory(factory.django.DjangoModelFactory):
    has_user = factory.Faker("pybool", truth_probability=50)
    user = factory.Maybe("has_user", factory.SubFactory(UserFactory), None)
    original_absolute_url = factory.Faker("url")
    short_relative_url = factory.LazyAttribute(lambda instance: generate_short_link(instance.original_absolute_url))
    is_public = factory.Faker("pybool")
    created_at = factory.LazyFunction(now)

    class Meta:
        model = Link
        exclude = ("has_user",)


class VisitFactory(factory.django.DjangoModelFactory):
    link = factory.SubFactory(LinkFactory)
    has_visitor_ip = factory.Faker("pybool", truth_probability=80)
    visitor_ip = factory.Maybe("has_visitor_ip", factory.Faker("ipv4"), None)
    user = factory.SelfAttribute("link.user")
    visited_at = factory.LazyFunction(now)

    class Meta:
        model = Visit
        exclude = ("has_visitor_ip",)
