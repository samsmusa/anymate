from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from store import models, serializers, protected_serializers
from xanymate import permissions
from django.db.models import Q, Count

@extend_schema(tags=["Private", "Private-store-collection"])
class PrivateStoreCollectionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', "post", "delete")
    queryset = models.StoreCollection.objects.all()
    serializer_class = serializers.StoreCollectionSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsCustomer, permissions.IsOwner]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return models.StoreCollection.objects.filter(created_by=self.request.user)


@extend_schema(tags=["Private", "Private-store-artifact"])
class PrivateStoreArtifactViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', "post", "put", "delete")
    queryset = models.StoreArtifact.objects.all()
    serializer_class = serializers.StoreArtifactsSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsCustomer, permissions.IsOwner]
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        return models.StoreArtifact.objects.filter(created_by=self.request.user)


@extend_schema(tags=["Protected", "Protected-store-collection"])
class ProtectedStoreCollectionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'post', "delete")
    queryset = models.StoreCollection.objects.all()
    serializer_class = protected_serializers.ProtectedStoreCollectionSerializer
    permission_classes = [permissions.IsAdmin]
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]

    @extend_schema(
        summary="List statistics of collections",
        description="Returns aggregated statistics for all collections and by collection_id.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "total": {"type": "integer", "description": "Total number of collections"},
                    "active": {"type": "integer", "description": "Number of active collections"},
                    "inactive": {"type": "integer", "description": "Number of inactive collections"},
                    "per_collection": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "collection_id": {"type": "integer", "description": "Collection ID"},
                                "total": {"type": "integer", "description": "Total artifacts in this collection"},
                                "active": {"type": "integer", "description": "Active artifacts in this collection"},
                                "inactive": {"type": "integer", "description": "Inactive artifacts in this collection"},
                            }
                        }
                    }
                }
            }
        }
    )
    @action(detail=False, methods=["get"], url_path="statistics")
    def statistics(self, request):
        """Custom endpoint to return statistics for all collections and per collection."""
        total = self.queryset.count()
        active = self.queryset.filter().count()
        inactive = total - active

        # Per collection statistics
        per_collection_stats = (
            self.queryset
            .values('id')  # collection_id
            .annotate(
                total=Count('id'),
                active=Count('id', filter=Q(is_active=True)),
                inactive=Count('id', filter=Q(is_active=False))
            )
        )
        data = {
            "total": total,
            "active": active,
            "inactive": inactive,
            "per_collection": list(per_collection_stats)
        }
        return Response(data)

    @extend_schema(
        summary="Statistics for a single collection",
        description="Returns statistics of artifacts within a specific collection.",
        responses={
            200: {
                "type": "object",
                "properties": {
                    "collection_id": {"type": "integer"},
                    "total": {"type": "integer"},
                    "active": {"type": "integer"},
                    "inactive": {"type": "integer"},
                }
            }
        }
    )
    @action(detail=True, methods=["get"], url_path="statistics")
    def statistics_detail(self, request, pk=None):
        collection = self.get_object()
        total = collection.storeartifact_set.count()
        active = collection.storeartifact_set.filter(is_active=True).count()
        inactive = total - active
        return Response({
            "collection_id": collection.id,
            "total": total,
            "active": active,
            "inactive": inactive,
        })


@extend_schema(tags=["Protected", "Protected-store-artifact"])
class ProtectedStoreArtifactViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', "post", "put", "delete")
    queryset = models.StoreArtifact.objects.all()
    serializer_class = protected_serializers.ProtectedStoreArtifactSerializer
    lookup_field = 'pk'
    permission_classes = [permissions.IsAdmin]
    filter_backends = [DjangoFilterBackend]
