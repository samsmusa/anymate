from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets

from store import models, serializers, protected_serializers
from xanymate import permissions


@extend_schema(tags=["private-store-collection"])
class PrivateStoreCollectionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', "post", "delete")
    queryset = models.StoreCollection.objects.all()
    serializer_class = serializers.StoreCollectionSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsCustomer, permissions.IsOwner]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return models.StoreCollection.objects.filter(created_by=self.request.user)


@extend_schema(tags=["private-store-artifact"])
class PrivateStoreArtifactViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', "post", "put", "delete")
    queryset = models.StoreArtifact.objects.all()
    serializer_class = serializers.StoreArtifactsSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsCustomer, permissions.IsOwner]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return models.StoreArtifact.objects.filter(created_by=self.request.user)


@extend_schema(tags=["protected-store-collection"])
class ProtectedStoreCollectionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', "delete")
    queryset = models.StoreCollection.objects.all()
    serializer_class = protected_serializers.ProtectedStoreCollectionSerializer
    permission_classes = [permissions.IsAdmin]
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]


@extend_schema(tags=["protected-store-artifact"])
class ProtectedStoreArtifactViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', "post", "put", "delete")
    queryset = models.StoreArtifact.objects.all()
    serializer_class = protected_serializers.ProtectedStoreArtifactSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdmin]
    filter_backends = [DjangoFilterBackend]
