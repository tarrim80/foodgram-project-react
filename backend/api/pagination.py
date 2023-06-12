from rest_framework.pagination import PageNumberPagination


class LimitPageNumberPagination(PageNumberPagination):
    """Определение стиля пагинации с указателем запроса `limit`."""
    page_size = 6
    page_size_query_param = 'limit'
