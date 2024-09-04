from rest_framework import serializers

from BookStoreApp.models import Book


# Create a serializer class for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn']
        # fields = '__all__'
