from django.urls import path

from core import views

urlpatterns = [
    path("", views.chart, name="chart"),
    path("year/", views.yearly_avg_co2, name="year"),
]
