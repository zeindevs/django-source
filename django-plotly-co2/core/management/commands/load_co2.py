import csv
from datetime import date
from itertools import islice
from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import CO2


class Command(BaseCommand):
    help = "Load data from CO2 file"

    def handle(self, *args, **options):
        datafile = settings.BASE_DIR / "data" / "monthly_in_situ_co2_mlo.csv"

        with open(datafile, "r") as f:
            reader = csv.DictReader(islice(f, 61, None))

            for row in reader:
                dt = date(
                    year=int(row["Yr"]),
                    month=int(row["Mn"]),
                    day=1,
                )
                CO2.objects.get_or_create(date=dt, average=row["CO2"])
