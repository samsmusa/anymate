from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from ui import views

urlpatterns = [
    path('', views.index, name='index'),
]
