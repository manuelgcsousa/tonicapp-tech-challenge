from rest_framework.pagination import PageNumberPagination


class SingleSetPagination(PageNumberPagination):
    page_size = 2
    max_page_size = 1000
    page_query_param = 'page'
    page_size_query_param = 'per_page'

