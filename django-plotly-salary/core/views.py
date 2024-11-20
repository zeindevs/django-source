from django.db.models import Avg, Case, CharField, Value, When
from django.shortcuts import render
import plotly.express as px

from core.models import PersonSalary


# Create your views here.
def scatter(request):
    person_salaries = PersonSalary.objects.filter(
        education__in=["1. < HS Grad", "5. Advanced Degree"]
    )
    ages = person_salaries.values_list("age", flat=True)
    salaries = person_salaries.values_list("salary", flat=True)
    color = person_salaries.values_list("education", flat=True)

    fig = px.scatter(
        x=ages,
        y=salaries,
        title="Salary by Age",
        height=600,
        color=color,
        trendline="ols",
    )
    chart = fig.to_html()

    context = {"chart": chart}
    return render(request, "scatter.html", context)


def box(request):
    person_salaries = PersonSalary.objects.all()

    # 15-19, 20-24, 25-29, etc
    YEARS_PER_AGG = 5
    age_bins = [(i, i + YEARS_PER_AGG - 1) for i in range(15, 85, YEARS_PER_AGG)]
    conditions = [When(age__range=bin, then=Value(f"{bin}")) for bin in age_bins]

    case = Case(*conditions, output_field=CharField())

    age_groupings = (
        person_salaries.annotate(age_group=case)
        .values("age_group")
        .order_by("age_group")
    )

    ages_groups = age_groupings.values_list("age_group", flat=True)
    salaries = person_salaries.values_list("salary", flat=True)

    fig = px.box(
        x=ages_groups,
        y=salaries,
        title="Salary by Age",
        height=600,
    )
    chart = fig.to_html()

    context = {"chart": chart}
    return render(request, "scatter.html", context)


def line(request):
    person_salaries = PersonSalary.objects.all()

    # 15-19, 20-24, 25-29, etc
    YEARS_PER_AGG = 5
    age_bins = [(i, i + YEARS_PER_AGG - 1) for i in range(15, 85, YEARS_PER_AGG)]
    conditions = [When(age__range=bin, then=Value(f"{bin}")) for bin in age_bins]

    case = Case(*conditions, output_field=CharField())

    age_groupings = (
        person_salaries.annotate(age_group=case)
        .values("age_group")
        .order_by("age_group")
        .annotate(avg=Avg("salary"))
    )

    ages_groups = age_groupings.values_list("age_group", flat=True)
    salaries = age_groupings.values_list("avg", flat=True)

    fig = px.line(
        x=ages_groups,
        y=salaries,
        title="Salary by Age",
        height=600,
    )
    chart = fig.to_html()

    context = {"chart": chart}
    return render(request, "scatter.html", context)
