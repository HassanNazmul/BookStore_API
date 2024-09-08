from django.contrib.auth.models import UserManager
from django.db import models


# Create your models here.


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    created_by = models.ForeignKey(UserManager, on_delete=models.CASCADE, related_name='author')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
