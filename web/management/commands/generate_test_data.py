from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError

from web.factories import VisitFactory


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--amount", type=int, default=1000,
                            help="Количество объектов Visit для генерирования (по умолчанию 1000).")

    def handle(self, *args, **options):
        count = 0

        for _ in range(options["amount"]):
            try:
                VisitFactory.create()
                count += 1
            except IntegrityError:
                pass

        print(f"Успешно создано {count} посещений.")
