from django.db import models


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False, null=False)
    # author = models.CharField(max_length=50, blank=False, null=False)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    published_date = models.DateField(blank=False, null=False)
    isbn = (models.CharField(max_length=20, unique=True, blank=False, null=False))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Author(models.Model):
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    nationality = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
