from unicodedata import category

from rest_framework import serializers
from setuptools.config.pyprojecttoml import validate

from BookStoreApp.models import Author, Category, Book


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio', 'age']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']


class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()
    categories = CategorySerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'categories', 'published_date', 'created_at', 'updated_at']

    # Overriding the create method to handle nested data in the request
    # This method will be called when we call serializer.save() in the view
    def create(self, validated_data):
        author_data = validated_data.pop('author')  # Extract author data from the request

        # Check if the author data is an instance of Author
        author_name = author_data.get('name')  # Extract author name from the author data
        author, created = Author.objects.get_or_create(name=author_name,
                                                       defaults=author_data)  # Get or create the author object

        categories_data = validated_data.pop('categories')  # Extract categories data from the request
        if not categories_data:
            raise serializers.ValidationError({"categories": "This field cannot be empty."})

        # Create the book with the found or newly created author
        book = Book.objects.create(author=author, **validated_data)

        # Loop through the categories data and add them to the book
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(**category_data)
            book.categories.add(category)

        return book
