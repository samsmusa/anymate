from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from saas import models, serializers, filters


@extend_schema(tags=["public-services"])
class PublicServicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ServiceFilter
