from django.contrib.auth.models import User
from django.db import models
from model_utils.models import TimeStampedModel

from core import utils


# Create your models here.
class Repository(TimeStampedModel):
    name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = "Repositories"

    def __str__(self):
        return f"{self.name}"


class Commit(TimeStampedModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commits")
    repository = models.ForeignKey(Repository, on_delete=models.CASCADE)
    code = models.TextField()
    hash = models.CharField(max_length=40, default=utils.generate_hash)

    def __str__(self):
        return f"commit {self.hash}"
