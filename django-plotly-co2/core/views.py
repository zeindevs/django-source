from django.db.models import Avg
import plotly.express as px
from django.shortcuts import render

from core.models import CO2
from core.forms import DateForm


# Create your views here.
def chart(request):
    co2 = CO2.objects.all()
    start = request.GET.get("start")
    end = request.GET.get("end")

    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
        title="CO2 PPM",
        labels={"x": "Date", "y": "CO2 PPM"},
    )
    fig.update_layout(
        title={
            "font_size": 22,
            "xanchor": "center",
            "x": 0.5,
        }
    )
    chart = fig.to_html()

    context = {"chart": chart, "form": DateForm()}
    return render(request, "chart.html", context)


def yearly_avg_co2(request):
    averages = CO2.objects.values("date__year").annotate(avg=Avg("average"))
    x = averages.values_list("date__year", flat=True)
    y = averages.values_list("avg", flat=True)

    text = [f"{avg:.1f}" for avg in y]

    fig = px.bar(x=x, y=y, text=text)
    fig.update_layout(
        title_text="Average CO2 concentration per year",
        yaxis_range=[0, 500],
    )
    fig.update_traces(
        textfont_size=12, textangle=0, textposition="outside", cliponaxis=False
    )

    chart = fig.to_html()
    context = {"chart": chart}
    return render(request, "chart.html", context)
