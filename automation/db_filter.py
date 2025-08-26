import django_filters
from . import models

class ExecutionEntityFilter(django_filters.FilterSet):
    finished = django_filters.BooleanFilter()
    mode = django_filters.CharFilter(lookup_expr='iexact')
    status = django_filters.CharFilter(lookup_expr='iexact')
    workflowid = django_filters.CharFilter(field_name='workflowid__id', lookup_expr='iexact')
    startedat_after = django_filters.DateTimeFilter(field_name='startedat', lookup_expr='gte')
    startedat_before = django_filters.DateTimeFilter(field_name='startedat', lookup_expr='lte')

    class Meta:
        model = models.ExecutionEntity
        fields = ['finished', 'mode', 'status', 'workflowid', 'startedat_after', 'startedat_before']
