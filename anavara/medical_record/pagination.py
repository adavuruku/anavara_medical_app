from rest_framework import pagination

class CustomPagination(pagination.LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'per_page'
    offset_query_param = 'page'
    max_limit = 2