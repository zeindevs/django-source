from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from devices.api import app

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', app.urls),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
