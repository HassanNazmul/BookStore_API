from django.shortcuts import render
from rest_framework import viewsets

from BookStoreApp.models import Author, Category, Book
from BookStoreApp.serializers import AuthorSerializer, CategorySerializer, BookSerializer


# Create your views here.
class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
