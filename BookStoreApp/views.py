from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from BookStoreApp.filters import BookFilter
from BookStoreApp.models import Book
from BookStoreApp.serializers import BookSerializer

from BookStoreApp.pagination import paginate_queryset


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

            # Apply filters to the queryset
            filterset = BookFilter(request.GET, queryset=books)
            if filterset.is_valid():
                books = filterset.qs

            # If no books are found, return a message
            if not books.exists():
                return Response({'No Books Available in the Record'}, status=status.HTTP_200_OK)

            # Apply pagination to the books queryset
            paginated_books, paginator = paginate_queryset(books, request)

            # Serialize the paginated data
            serializer = BookSerializer(paginated_books, many=True)

            # Return the paginated response
            return paginator.get_paginated_response(serializer.data)

    # If the ID provided is invalid, return a message
    except Book.DoesNotExist:
        return Response({f'Invalid ID in the URL, There is no Book with ID {id}'},
                        status=status.HTTP_404_NOT_FOUND)

    # If any other error occurs, return the error message
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def create_book(request):
    try:
        # For single book creation, use the existing logic
        serializer = BookSerializer(data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Book created successfully', **serializer.data},
                            status=status.HTTP_201_CREATED)

        # If the data is invalid, return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
def bulk_create_books(request):
    try:
        # Check if the incoming data is a list (bulk request)
        if not isinstance(request.data, list):
            return Response({'error': 'This endpoint is for bulk creation only. Please provide a list of books.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # For bulk creation, we validate each book
        bulk_errors = []
        created_books = []

        for book_data in request.data:
            serializer = BookSerializer(data=book_data, context={'request': request})

            if serializer.is_valid():
                serializer.save()
                created_books.append(serializer.data)  # Add the created book to the list
            else:
                # Include the title or another identifier along with the error
                bulk_errors.append({
                    'book': book_data.get('title', 'Unknown Title'),
                    'errors': serializer.errors
                })  # Track errors for individual books

        # If any errors occurred during bulk creation, return them
        if bulk_errors:
            return Response({
                'message': 'Some books were not created due to errors',
                'errors': bulk_errors,
                'created_books': created_books
            }, status=status.HTTP_400_BAD_REQUEST)

        # If all books were created successfully, return the created data
        return Response({
            'message': 'Books created successfully',
            'data': created_books
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
