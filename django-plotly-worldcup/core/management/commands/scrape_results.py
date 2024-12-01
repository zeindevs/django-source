from typing import List
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand
from django.utils import timezone

from core.models import Fixture


class Command(BaseCommand):
    help = "Load data"

    def handle(self, *args, **options):
        urls = self.construct_urls()
        for url in urls:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            results = soup.select("ul.ssrcss-1w89ukb-StackLayout>li")
            for result in results:
                home = result.select_one(
                    "div.ssrcss-bon2fo-WithInlineFallback-TeamHome>div>div>span.ssrcss-1p14tic-DesktopValue"
                ).text
                away = result.select_one(
                    "div.ssrcss-nvj22c-WithInlineFallback-TeamAway>div>div>span.ssrcss-1p14tic-DesktopValue"
                ).text
                goals = result.select("div.ssrcss-mufdym-StyledScore>div")
                home_goals = goals[0].text
                away_goals = goals[2].text
                Fixture.objects.get_or_create(
                    team1=home,
                    team2=away,
                    team1_goals=home_goals,
                    team2_goals=away_goals,
                )

    def construct_urls(self) -> List[str]:
        BASE_URL = "https://www.bbc.com/sport/football/scores-fixtures"
        START_DATE = timezone.datetime(year=2024, month=11, day=1)
        END_DATE = timezone.datetime(year=2024, month=11, day=7)
        delta = (END_DATE - START_DATE).days

        urls = []
        for i in range(delta + 1):
            date = START_DATE + timezone.timedelta(days=i)
            date = date.strftime("%Y-%m-%d")
            urls.append(f"{BASE_URL}/{date}")

        return urls
