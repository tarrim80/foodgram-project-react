from django.conf import settings
from rest_framework.pagination import PageNumberPagination


class PageNumberPaginationLimit(PageNumberPagination):
    """Пагинация с параметром запроса `limit`."""
    page_size = settings.PAGE_SIZE
    page_size_query_param = 'limit'
