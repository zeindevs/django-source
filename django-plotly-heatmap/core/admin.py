from django.contrib import admin

from core.models import Commit, Repository

# Register your models here.
admin.site.register(Repository)
admin.site.register(Commit)
