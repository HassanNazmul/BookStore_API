from rest_framework import filters


class BookSearchFilter(filters.SearchFilter):
    search_param = 'search'

    # Fields to be searched
    search_fields = ['title', 'author__first_name', 'author__last_name', 'isbn', 'author__nationality', ]
