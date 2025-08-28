from datetime import timedelta

from django.db.models import Count, Min, Avg, Max, Sum
from django.db.models.functions import TruncDate
from django.utils.timezone import now
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

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


@extend_schema(tags=["Protected", "Protected-automate-engine"])
class WorkflowStatisticsView(APIView):
    """
    API to provide statistics for WorkflowEntity.
    """
    permission_classes = [permissions.IsAdminUser]  # restrict access to admins

    def get(self, request, *args, **kwargs):
        total_workflows = models.WorkflowEntity.objects.count()
        active_workflows = models.WorkflowEntity.objects.filter(active=True).count()
        archived_workflows = models.WorkflowEntity.objects.filter(isarchived=True).count()
        total_triggers = models.WorkflowEntity.objects.aggregate(total=Count('triggercount'))['total'] or 0

        # Workflows created in the last 7 days
        last_7_days = now() - timedelta(days=7)
        workflows_last_week = models.WorkflowEntity.objects.filter(createdat__gte=last_7_days).count()

        # Optional: trigger count stats
        trigger_stats = models.WorkflowEntity.objects.aggregate(
            min_trigger=Min('triggercount'),
            max_trigger=Max('triggercount'),
            avg_trigger=Avg('triggercount')
        )

        # Workflows by active/archived status
        by_status = models.WorkflowEntity.objects.values('active', 'isarchived').annotate(count=Count('id'))

        data = {
            "total_workflows": total_workflows,
            "active_workflows": active_workflows,
            "archived_workflows": archived_workflows,
            "total_triggers": total_triggers,
            "workflows_last_week": workflows_last_week,
            "trigger_stats": trigger_stats,
            "by_status": list(by_status),
        }

        return Response(data)


@extend_schema(tags=["Protected", "Dashboard"])
class WorkflowDashboardView(APIView):
    """
    Dashboard statistics for workflows based on WorkflowStatistics model.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        qs = models.WorkflowStatistics.objects.all()

        total_workflows = qs.values('workflowid').distinct().count()
        total_events = qs.aggregate(total=Sum('count'))['total'] or 0

        # Success & error events
        success_events = qs.filter(name__icontains="success").aggregate(total=Sum('count'))['total'] or 0
        error_events = qs.filter(name__icontains="error").aggregate(total=Sum('count'))['total'] or 0

        latest_event = qs.aggregate(latest=Max('latestevent'))['latest']
        avg_root_count = qs.aggregate(avg=Avg('rootcount'))['avg'] or 0
        total_root_count = qs.aggregate(total=Sum('rootcount'))['total'] or 0

        # Top 5 workflows by total events
        top_workflows = qs.values('workflowid__id', 'name').annotate(total_count=Sum('count')).order_by('-total_count')[
            :5]

        data = {
            "total_workflows": total_workflows,
            "total_events": total_events,
            "success_events": success_events,
            "error_events": error_events,
            "latest_event": latest_event,
            "average_root_count": avg_root_count,
            "total_root_count": total_root_count,
            "top_workflows": list(top_workflows)
        }

        return Response(data)


@extend_schema(tags=["Protected", "Dashboard"])
class WorkflowStatisticsGraphView(APIView):
    """
    Provides workflow usage counts for the last 7, 15, and 30 days
    for dashboard graph/bar chart visualization.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        today = now().date()
        periods = {"7_days": 7, "15_days": 15, "30_days": 30}
        result = {}

        for label, days in periods.items():
            start_date = today - timedelta(days=days - 1)
            qs = models.WorkflowStatistics.objects.filter(latestevent__date__gte=start_date)

            # Aggregate counts per day using TruncDate
            usage_per_day = (
                qs.annotate(day=TruncDate("latestevent"))
                .values("day")
                .annotate(total_events=Sum("count"))
                .order_by("day")
            )

            # Fill missing dates with 0
            usage_dict = {str(today - timedelta(days=i)): 0 for i in range(days - 1, -1, -1)}
            for item in usage_per_day:
                usage_dict[str(item["day"])] = item["total_events"]

            result[label] = usage_dict

        return Response(result)


@extend_schema(tags=["Protected", "Dashboard"])
class WorkflowEntityUsageGraphView(APIView):
    """
    Provides workflow creation counts for WorkflowEntity
    over the last 7, 15, and 30 days for dashboard charts.
    """
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        today = now().date()
        periods = {"7_days": 7, "15_days": 15, "30_days": 30}
        result = {}

        for label, days in periods.items():
            start_date = today - timedelta(days=days - 1)
            qs = models.WorkflowEntity.objects.filter(createdat__date__gte=start_date)

            # Aggregate counts per day using TruncDate
            usage_per_day = (
                qs.annotate(day=TruncDate("createdat"))
                .values("day")
                .annotate(total_workflows=Count("id"))
                .order_by("day")
            )

            # Fill missing dates with 0
            usage_dict = {str(today - timedelta(days=i)): 0 for i in range(days - 1, -1, -1)}
            for item in usage_per_day:
                usage_dict[str(item["day"])] = item["total_workflows"]

            result[label] = usage_dict

        return Response(result)
