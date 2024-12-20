import calendar
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils import timezone
import plotly.express as px

from .models import Commit
from . import utils


# Create your views here.
@login_required()
def commits(request):
    commits = Commit.objects.filter(user=request.user).order_by("created")
    now = timezone.now()
    start = now - timezone.timedelta(days=364)
    daterange = utils.date_range(start, now)
    counts = [[] for _ in range(7)]
    dates = [[] for _ in range(7)]

    for dt in daterange:
        count = commits.filter(created__date=dt).count()
        day_number = dt.weekday()
        counts[day_number].append(count)
        dates[day_number].append(dt)

    day_names = list(calendar.day_name)
    first_day = daterange[0].weekday()
    days = day_names[first_day:] + day_names[:first_day]
    fig = px.imshow(
        counts,
        labels={'color': 'commit'},
        color_continuous_scale="greens",
        x=dates[0],
        y=days,
        # height=320,
        # width=1300,
    )
    fig.update_layout(plot_bgcolor="white")
    fig.update_traces({"xgap": 5, "ygap": 5})
    chart = fig.to_html()

    context = {"chart": chart}
    return render(request, "commits.html", context)
