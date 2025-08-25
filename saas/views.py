from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from saas import models, serializers, filters, protected_serializers
from xanymate import permissions


@extend_schema(tags=["public-services"])
class PublicServicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ServiceFilter


@extend_schema(tags=["private-service-subscriptions"])
class PrivateServiceSubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'put', 'patch', "post")
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsCustomer]
    filter_backends = [DjangoFilterBackend]
    # filterset_class = filters.ServiceFilter

    def get_queryset(self):
        return models.Subscription.objects.filter(created_by=self.request.user)


@extend_schema(tags=["protected-services"])
class ProtectedServicesViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'put', 'patch')
    queryset = models.Service.objects.all()
    serializer_class = protected_serializers.ProtectedServiceSerializer
    permission_classes = [permissions.IsAdmin]
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ServiceFilter


@extend_schema(tags=["Protected-service-subscriptions"])
class ProtectedServiceSubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'put', 'patch', "delete")
    queryset = models.Subscription.objects.all()
    serializer_class = protected_serializers.ProtectedSubscriptionSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdmin]
    filter_backends = [DjangoFilterBackend]
    # filterset_class = filters.ServiceFilter



