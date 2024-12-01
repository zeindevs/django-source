from django.db.models import Q
from django.shortcuts import render
import plotly.express as px

from core.models import Fixture


# Create your views here.
def scores(request):
    fixtures = Fixture.objects.all()
    teams = fixtures.values_list("team1", flat=True).distinct()
    goals = {}
    for team in teams:
        team_fixtures = fixtures.filter(Q(team1=team) | Q(team2=team))
        total_goals = sum([fix.get_goals(team) for fix in team_fixtures])
        goals[team] = total_goals

    goals = dict(sorted(goals.items(), key=lambda x: x[1], reverse=True))
    fig = px.bar(x=goals.keys(), y=goals.values(), title="Football")
    chart = fig.to_html()

    context = {"chart": chart}
    return render(request, "index.html", context)
