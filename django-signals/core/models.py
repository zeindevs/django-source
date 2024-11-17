from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    cv = models.FileField(upload_to="cvs/", null=True, blank=True)
