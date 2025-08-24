from django.contrib.auth import views as auth_views
from django.urls import path, re_path

from ui import views

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/profile', views.dashboard, name='dashboard_profile'),
    # path('dashboard/services', views.dashboard_services, name='dashboard_services'),
    path('dashboard/services', views.DashboardServiceView.as_view(), name='dashboard_services'),
    path(
        "dashboard/service-requests/",
        views.DashboardServiceRequestsView.as_view(),
        name="dashboard_service_requests",
    ),
    path(
        "dashboard/manage-service/<int:subscription_id>/",
        views.DashboardServiceManageView.as_view(),
        name="dashboard_service_manage",
    ),
    re_path(
        r"^dashboard/manage-service/(?P<subscriptone_id>\d+)(?:/(?P<page_name>\w+))?/?$",
        views.DashboardServiceRequestsView.as_view(),
        name="dashboard_service_manage",
    ),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),

    path("logout/", auth_views.LogoutView.as_view(), name="logout"),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='pages/auth/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='pages/auth/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='pages/auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='pages/auth/password_reset_complete.html'),
         name='password_reset_complete'),
]
