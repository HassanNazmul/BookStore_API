from django.urls import path

from BookStoreApp import views

urlpatterns = [
    path('books/', views.get_books),
    path('books/<int:id>/', views.get_books)
]
