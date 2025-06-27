from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError

class CustomPageNumberPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 100

    def paginate_queryset(self, queryset, request, view=None):
        page = request.query_params.get(self.page_query_param)
        page_size = request.query_params.get(self.page_size_query_param)

        # Validate presence of page and page_size if you want to enforce it
        if page is None:
            raise ValidationError({"page": "This query parameter is required."})
        if page_size is None:
            raise ValidationError({"page_size": "This query parameter is required."})

        try:
            page_num = int(page)
            page_sz = int(page_size)
        except ValueError:
            raise ValidationError({"detail": "page and page_size must be integers."})

        if page_num < 1:
            raise ValidationError({"page": "page must be >= 1."})
        if page_sz < 1 or page_sz > self.max_page_size:
            raise ValidationError({"page_size": f"page_size must be between 1 and {self.max_page_size}."})

        self.page_size = page_sz
        return super().paginate_queryset(queryset, request, view)
