from django.urls import path

from BookStoreApp import views
from BookStoreApp.views import create_book

urlpatterns = [
    path('books/', views.get_books),
    path('books/<int:id>/', views.get_books),
    path('books/create/', create_book, name='create-book'),
    path('books/bulk/', views.bulk_create_books),
]
