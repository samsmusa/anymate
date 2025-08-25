import django_filters
from saas import models


class ServiceFilter(django_filters.FilterSet):
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = models.Service
        fields = ['is_active']
