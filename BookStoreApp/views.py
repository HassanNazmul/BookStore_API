import logging

from django.db import transaction
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from BookStoreApp.models import Book
from BookStoreApp.serializers import BookSerializer


# Create your views here.
class BookAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # Get the id from the request
        id = kwargs.get('id', None)
        # If id is not None, get the book with the id
        if id is not None:
            try:  # Try to get the book with the id
                book = get_object_or_404(Book, id=id)
                serializer = BookSerializer(book)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Http404:  # If the book with the id is not found, return a 404 response
                return Response({"message": "Invalid id"}, status=status.HTTP_404_NOT_FOUND)
        else:
            try:  # Get all the books
                books = Book.objects.all()
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Http404:  # If no books are found, return a 404 response
                return Response({"message": "No books found"}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, *args, **kwargs):
        book_serializer = BookSerializer(data=request.data)

        if book_serializer.is_valid():
            try:
                # Save the valid data and create the book
                book_serializer.save()
                return Response({'message': 'Book created successfully', **book_serializer.data},
                                status=status.HTTP_201_CREATED)
            except Exception as e:
                # Log the exception for internal purposes
                logging.error(f"Error while creating book: {str(e)}")
                return Response({'message': 'An internal error occurred. Please try again later.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                                )

        # If the data is invalid, return errors
        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, *args, **kwargs):
        # Get the book ID from the URL
        book_id = kwargs.get('id', None)

        # Retrieve the book instance
        book = get_object_or_404(Book, id=book_id)

        # Pass the request context when creating the serializer
        book_serializer = BookSerializer(book, data=request.data, context={'request': request})

        if book_serializer.is_valid():
            try:
                # Save the updated book instance
                book_serializer.save()
                return Response(
                    {'message': 'Book updated successfully', **book_serializer.data},
                    status=status.HTTP_200_OK
                )
            except Exception as e:
                # Log any unexpected errors
                logging.error(f"Error while updating book: {str(e)}")
                return Response(
                    {'message': 'An internal error occurred. Please try again later.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        # Return validation errors if the data is not valid
        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        # Get ID from the request
        book_id = kwargs.get('id', None)
        # Try to get the book Object
        book = get_object_or_404(Book, id=book_id)
        # Partial update the book object
        book_serializer = BookSerializer(book, data=request.data, partial=True)

        if book_serializer.is_valid():
            try:
                # Save the valid data and update the book
                book_serializer.save()
                return Response({'message': 'Book updated successfully', **book_serializer.data},
                                status=status.HTTP_200_OK)
            except Exception as e:
                # Log the exception for internal purposes
                logging.error(f"Error while updating book: {str(e)}")
                return Response({'message': 'An internal error occurred. Please try again later.'},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR
                                )

        # If the data is invalid, return errors
        return Response(book_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        # Get the book ID from the URL
        book_id = kwargs.get('id', None)
        # Retrieve the book instance or return 404 if not found
        book = get_object_or_404(Book, id=book_id)

        try:
            # Use atomic transaction for safety in case of cascading delete logic
            with transaction.atomic():
                # Delete the book instance
                book.delete()
            # Return a 200 OK response with a confirmation message
            return Response({'message': 'Book deleted successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            # Log any unexpected errors with more details
            logging.error(f"Error while deleting book (ID: {book_id}): {str(e)}")
            # Return an internal server error message
            return Response(
                {'message': 'An internal error occurred. Please try again later.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
