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
              ] + private_router.urls
