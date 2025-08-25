from django.urls import path, include
from rest_framework_nested import routers

from saas import rest_views

public_router = routers.DefaultRouter()

public_router.register(r'services', rest_views.PublicServicesViewSet, basename='public-service')

urlpatterns = [
    path(r'public/', include(public_router.urls)),
]
