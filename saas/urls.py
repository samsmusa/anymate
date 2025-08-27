from django.urls import path, include
from rest_framework_nested import routers

from saas import views

public_router = routers.DefaultRouter()
private_router = routers.DefaultRouter()
protected_router = routers.DefaultRouter()

public_router.register(r'services', views.PublicServicesViewSet, basename='public-service')
private_router.register(r'subscriptions', views.PrivateServiceSubscriptionViewSet, basename='private-service')

protected_router.register(r'services', views.ProtectedServicesViewSet, basename='protected-service')
protected_router.register(r'subscriptions', views.ProtectedServiceSubscriptionViewSet,
                          basename='protected-subscription')

urlpatterns = [
    path(r'public/', include(public_router.urls)),
    path(r'private/', include(private_router.urls)),
    path(r'protected/', include(protected_router.urls)),
    path("service-sidebar/", views.ServiceSidebarView.as_view(), name="service-sidebar"),
]
