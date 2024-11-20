import csv
from django.core.management.base import BaseCommand
from django.conf import settings

from core.models import PersonSalary


class Command(BaseCommand):
    help = "Load data from wage file"

    def handle(self, *args, **options):
        if PersonSalary.objects.count() > 0:
            PersonSalary.objects.all().delete()

        DATA_FILE = settings.BASE_DIR / "data" / "wage.csv"
        assert DATA_FILE.exists()

        with open(DATA_FILE, "r") as f:
            reader = csv.DictReader(f)
            db_rows = []
            for row in reader:
                db_rows.append(
                    PersonSalary(
                        age=row["age"],
                        education=row["education"],
                        salary=row["wage"],
                    )
                )
            PersonSalary.objects.bulk_create(db_rows, batch_size=1000)
