from mongoengine.queryset.visitor import Q as QNode
from rest_framework.filters import SearchFilter
class SearchFilter(SearchFilter):
    def filter_queryset(self, request, queryset, view):

        search_fields = self.get_search_fields(view, request)
        search_terms = self.get_search_terms(request)

        if not search_fields or not search_terms:
            return queryset

        orm_lookups = [
            self.construct_search(six.text_type(search_field))
            for search_field in search_fields
        ]

        base = queryset  # base查询数据集
        conditions = []
        for search_term in search_terms: 
            queries = [
                # models.Q(**{orm_lookup: search_term})
                QNode(**{orm_lookup: search_term})
                for orm_lookup in orm_lookups
            ]
            conditions.append(reduce(operator.or_, queries))
        queryset = queryset.filter(reduce(operator.and_, conditions))
        return queryset
