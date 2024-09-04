from django.urls import path

from BookStoreApp import views

urlpatterns = [
    path('books/', views.BookAPIView.as_view(), name='book_list'),
    path('books/<int:id>/', views.BookAPIView.as_view(), name='book'),
]
