from django.urls import path
from rest_framework_nested import routers

from automation import views

private_router = routers.DefaultRouter()
private_router.register(r'annotation-tags', views.AnnotationTagEntityViewSet)
private_router.register(r'auth-sync-history', views.AuthProviderSyncHistoryViewSet)
private_router.register(r'credentials', views.CredentialsEntityViewSet)
private_router.register(r'event-destinations', views.EventDestinationsViewSet)
private_router.register(r'executions', views.ExecutionEntityViewSet)
private_router.register(r'workflows', views.WorkflowEntityViewSet)
private_router.register(r'workflows-statistics', views.WorkflowStatisticsViewSet, basename='workflow-statistics')

protected_router = routers.DefaultRouter()

urlpatterns = [
                  path("workflow/entity/statistics/", views.WorkflowStatisticsView.as_view(), name="workflow-statistics"),
                  path("workflow/entity/statistics/graph/", views.WorkflowEntityUsageGraphView.as_view(), name="workflow-statistics"),
                  path("workflow/statistics/view", views.WorkflowDashboardView.as_view(), name="workflow-statistics"),
                  path("workflow/statistics/graph/", views.WorkflowStatisticsGraphView.as_view(), name="workflow-statistics"),
              ] + private_router.urls
