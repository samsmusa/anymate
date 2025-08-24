from django.urls import path

from store import views

urlpatterns = [
    path('', views.StoreView.as_view(), name='store_home'),
    path('/collections', views.CollectionView.as_view(), name='store_collection'),
]
