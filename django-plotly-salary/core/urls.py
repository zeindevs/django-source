from django.urls import path

from core import views

urlpatterns = [
    path("scatter/", views.scatter),
    path("box/", views.box),
    path("line/", views.line),
]
