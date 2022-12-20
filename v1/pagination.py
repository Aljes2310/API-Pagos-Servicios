from rest_framework.pagination import PageNumberPagination

class SimplePagination(PageNumberPagination):
    page_size=10
    page_query_param="page_size"
    max_page_size=2000


class ReadPagination(PageNumberPagination):
    page_size=150
    page_query_param="page_size"