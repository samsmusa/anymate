from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions

from . import models, serializers, db_filter


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class AnnotationTagEntityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.AnnotationTagEntity.objects.all()
    serializer_class = serializers.AnnotationTagEntitySerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class AuthProviderSyncHistoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.AuthProviderSyncHistory.objects.all()
    serializer_class = serializers.AuthProviderSyncHistorySerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class CredentialsEntityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.CredentialsEntity.objects.all()
    serializer_class = serializers.CredentialsEntitySerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class EventDestinationsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.EventDestinations.objects.all()
    serializer_class = serializers.EventDestinationsSerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class ExecutionEntityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.ExecutionEntity.objects.all()
    serializer_class = serializers.ExecutionEntitySerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend]
    filterset_class = db_filter.ExecutionEntityFilter


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class WorkflowEntityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WorkflowEntity.objects.all()
    serializer_class = serializers.WorkflowEntitySerializer
    permission_classes = [permissions.IsAdminUser]


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class WorkflowStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.WorkflowStatistics.objects.all()
    serializer_class = serializers.WorkflowStatisticsSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = "workflow_id"
