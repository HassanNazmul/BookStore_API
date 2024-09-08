from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from BookStoreApp.models import Book
from BookStoreApp.serializers import BookSerializer


# Create your views here.

@api_view(['GET'])
def get_books(request):
    try:
        # Get all books from the database
        books = Book.objects.all().select_related('author')
        # if no data is found in the database
        if not books.exists():
            return Response({'No books available in the database'}, status=status.HTTP_404_NOT_FOUND)
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
