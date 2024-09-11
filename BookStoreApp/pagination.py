from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'results': data
        })


def paginate_queryset(queryset, request, page_size=7):
    """
    Utility function to paginate a queryset.
    """
    paginator = CustomPagination()
    paginator.page_size = page_size  # Set the page size here
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    return paginated_queryset, paginator
