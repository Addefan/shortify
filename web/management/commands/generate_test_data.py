from django.core.management.base import BaseCommand

from web.factories import VisitFactory
from web.models import Visit, User, Link


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--amount", type=int, default=1000,
                            help="Количество объектов Visit для генерирования (по умолчанию 1000).")

    def handle(self, *args, **options):
        visits = [VisitFactory.build() for _ in range(options["amount"])]
        links = [visit.link for visit in visits]
        users = [link.user for link in links if link.user is not None]

        users = User.objects.bulk_create(users, ignore_conflicts=True)
        links = Link.objects.bulk_create(links, ignore_conflicts=True)
        visits = Visit.objects.bulk_create(visits, ignore_conflicts=True)
        print(f"Успешно создано {len(users)} пользователей, {len(links)} ссылок и {len(visits)} посещений.")
