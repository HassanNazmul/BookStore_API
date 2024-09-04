from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False, null=False)
    author = models.CharField(max_length=50, blank=False, null=False)
    published_date = models.DateField(blank=False, null=False)
    isbn = (models.CharField(max_length=20, unique=True, blank=False, null=False))

    def __str__(self):
        return self.title
