from django.db import models

from BookStoreApp.models import Author


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=50, unique=True, blank=False, null=False)
    # author = models.CharField(max_length=50, blank=False, null=False)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    published_date = models.DateField(blank=False, null=False)
    isbn = (models.CharField(max_length=20, unique=True, blank=False, null=False))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

"""
book 10 object every obh has one author


"""