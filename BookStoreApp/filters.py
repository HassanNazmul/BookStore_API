from django_filters import rest_framework as filters
from BookStoreApp.models import Book


class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    # Corrected filtering by author's first and last name (with relation to the Author model)
    author_first_name = filters.CharFilter(field_name='author__first_name', lookup_expr='icontains')
    author_last_name = filters.CharFilter(field_name='author__last_name', lookup_expr='icontains')

    author_nationality = filters.CharFilter(field_name='author__nationality', lookup_expr='icontains')

    published_date = filters.DateFromToRangeFilter(field_name='published_date')

    class Meta:
        model = Book
        fields = ['title', 'author_first_name', 'author_last_name', 'author_nationality', 'published_date']
