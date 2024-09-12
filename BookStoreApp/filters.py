from django_filters import rest_framework as filters
from django.db.models import Q
from BookStoreApp.models import Book

class BookFilter(filters.FilterSet):
    title = filters.CharFilter(field_name='title', lookup_expr='icontains')

    # Corrected filtering by author's first and last name (with relation to the Author model)
    # author_first_name = filters.CharFilter(field_name='author__first_name', lookup_expr='icontains')
    # author_last_name = filters.CharFilter(field_name='author__last_name', lookup_expr='icontains')

    # Advanced filtering by author's first and last name with flexible matching
    author_name = filters.CharFilter(method='filter_author_name')

    published_date = filters.DateFromToRangeFilter(field_name='published_date')

    class Meta:
        model = Book
        fields = ['title', 'author_name', 'published_date']

    # Custom filter method for author_name to match both first and last name
    def filter_author_name(self, queryset, name, value):
        return queryset.filter(
            Q(author__first_name__icontains=value) | Q(author__last_name__icontains=value)
        )
