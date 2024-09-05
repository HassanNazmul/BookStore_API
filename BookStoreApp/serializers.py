import pycountry
from rest_framework import serializers

from BookStoreApp.models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['first_name', 'last_name', 'nationality']

    # Validation for first_name field
    def validate_first_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("First name should only contain alphabetic characters.")
        return value

    # Validation for last_name field
    def validate_last_name(self, value):
        if not value.isalpha():
            raise serializers.ValidationError("Last name should only contain alphabetic characters.")
        return value

    # Validation for nationality field using pycountry
    def validate_nationality(self, value):
        if not any(country.name == value for country in pycountry.countries):
            raise serializers.ValidationError("Nationality must be a valid country.")
        return value


# Create a serializer class for the Book model
class BookSerializer(serializers.ModelSerializer):
    # We still use AuthorSerializer for nested output but handle input validation manually
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'published_date', 'isbn', 'created_at']

    def create(self, validated_data):
        # Pop the author data from the validated data
        author_data = validated_data.pop('author')

        # After validation, check if the author already exists or create a new one
        author, created = Author.objects.get_or_create(
            first_name=author_data['first_name'],
            last_name=author_data['last_name'],
            defaults={'nationality': author_data.get('nationality', '')}
        )

        # If the author was already in the database and nationality was provided, update it
        if author_data.get('nationality'):
            author.nationality = author_data['nationality']
            author.save()

        # Create and return a new book instance
        book = Book.objects.create(author=author, **validated_data)
        return book

    def update(self, instance, validated_data):
        # Handle Partial updates for the author field if provided
        author_data = validated_data.pop('author', None)
        if author_data:
            author = instance.author
            author.first_name = author_data.get('first_name', author.first_name)
            author.last_name = author_data.get('last_name', author.last_name)
            author.nationality = author_data.get('nationality', author.nationality)
            author.save()

        # Update the book fields and return the updated instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
