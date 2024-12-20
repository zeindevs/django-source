from django.urls import path

from . import views
from .api import api

urlpatterns = [
    path("api/", api.urls),
    path("comments/", views.comments, name="comments"),
]
