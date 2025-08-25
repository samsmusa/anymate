from django.urls import path, include
from rest_framework_nested import routers

from store import views

private_router = routers.DefaultRouter()
protected_router = routers.DefaultRouter()

private_router.register(r'collections', views.PrivateStoreCollectionViewSet, basename='private-store-collection')
private_router.register(r'artifacts', views.PrivateStoreArtifactViewSet, basename='private-store-artifact')

protected_router.register(r'collections', views.ProtectedStoreCollectionViewSet, basename='protected-store-collection')
protected_router.register(r'artifacts', views.ProtectedStoreArtifactViewSet, basename='protected-store-artifact')

urlpatterns = [
    path(r'private/', include(private_router.urls)),
    path(r'protected/', include(protected_router.urls)),
]
