from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from BookStoreApp.models import Book
from BookStoreApp.serializers import BookSerializer


# Create your views here.

@api_view(['GET'])
def get_books(request, id=None):
    try:
        if id:
            # If an ID is provided, get the book with that ID
            book = Book.objects.get(id=id)
            serializer = BookSerializer(book)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # If no ID is provided, get all books
            books = Book.objects.all().select_related('author')
            # If no books are found, return a message
            if not books.exists():
                return Response({'No Books Available in the Record'}, status=status.HTTP_200_OK)
            serializer = BookSerializer(books, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
    # If the ID provided is invalid, return a message
    except Book.DoesNotExist:
        return Response({'Invalid ID in the URL'}, status=status.HTTP_404_NOT_FOUND)
    # If any other error occurs, return the error message
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
