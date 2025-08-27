from django import forms
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q, OuterRef, Exists
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views import View

from saas import models as saas_models
from saas.models import Subscription, Status, Service


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
        })
    )


class SignupForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            "placeholder": "Username",
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Password",
            "class": "block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm p-2"
        })
    )


def index(request):
    """Landing page"""
    return render(request, "index.html")


def login_view(request):
    """Login view"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = LoginForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username} 👋")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "pages/auth/login.html", {"form": form})


def signup_view(request):
    """Signup / registration view"""
    if request.user.is_authenticated:
        return redirect("dashboard")

    form = SignupForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
        else:
            user = User.objects.create_user(username=username, password=password)
            login(request, user)
            messages.success(request, f"Welcome, {user.username}! Your account has been created.")
            return redirect("dashboard")

    return render(request, "pages/auth/signup.html", {"form": form})


@login_required(login_url="login")
def dashboard(request):
    """Dashboard home"""
    return render(request, "index.html")


@login_required(login_url="login")
def dashboard_profile(request):
    """Dashboard profile page"""
    return render(request, "index.html")


#
# @login_required(login_url="login")
# def dashboard_services(request):
#     """Dashboard services page with search and pagination"""
#     search_query = request.GET.get('search', '')
#
#     services = saas_models.Service.objects.all().order_by('-created_at')
#
#     if search_query:
#         services = services.filter(
#             Q(name__icontains=search_query) |
#             Q(description__icontains=search_query)
#         )
#
#     paginator = Paginator(services, 8)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#
#     context = {
#         'services': page_obj,
#         'search_query': search_query,
#         'total_services': services.count(),
#     }
#
#     return render(request, "pages/dashboard/services.html", context)
#

class DashboardServiceView(LoginRequiredMixin, View):
    """Handles listing, updating, and deleting subscriptions in the dashboard"""

    login_url = "login"

    def test_func(self):
        """Only superusers can update or delete subscriptions"""
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')

        services = saas_models.Service.objects.all().order_by('-created_at')

        if search_query:
            services = services.filter(
                Q(name__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        subscriptions = saas_models.Subscription.objects.filter(
            user=request.user, service=OuterRef("pk")
        )
        services = services.annotate(subscribed=Exists(subscriptions))

        paginator = Paginator(services, 8)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        context = {
            'services': page_obj,
            'search_query': search_query,
            'total_services': services.count(),
        }
        return render(request, "index.html", context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        service_id = request.POST.get("service_id")

        service = get_object_or_404(saas_models.Service, id=service_id)

        if action == "subscribe":
            try:
                ins = saas_models.Subscription.objects.create(service=service, user=request.user)
                ins.save()
                messages.success(request, f"Request for subscription was successful")

            except Exception as e:
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": str(e)})
                messages.error(request, f"Error updating status: {str(e)}")

        return redirect("dashboard_services")


class DashboardServiceRequestsView(LoginRequiredMixin, UserPassesTestMixin, View):
    """Handles listing, updating, and deleting subscriptions in the dashboard"""

    login_url = "login"

    def test_func(self):
        """Only superusers can update or delete subscriptions"""
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        search_query = request.GET.get("search", "")
        status_filter = request.GET.get("status", "")

        subscriptions = Subscription.objects.select_related("user", "service").all().order_by("-started_at")

        if search_query:
            subscriptions = subscriptions.filter(
                Q(service__name__icontains=search_query)
                | Q(user__username__icontains=search_query)
                | Q(user__first_name__icontains=search_query)
                | Q(user__last_name__icontains=search_query)
            )

        if status_filter:
            subscriptions = subscriptions.filter(status=status_filter)

        paginator = Paginator(subscriptions, 8)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)

        context = {
            "service_requests": page_obj,
            "search_query": search_query,
            "status_filter": status_filter,
            "total_requests": subscriptions.count(),
            "status_choices": Status.choices,
        }
        return render(request, "index.html", context)

    def post(self, request, *args, **kwargs):
        action = request.POST.get("action")
        subscription_id = request.POST.get("subscription_id")

        subscription = get_object_or_404(Subscription, id=subscription_id)

        if action == "update_status":
            try:
                new_status = int(request.POST.get("status"))
                subscription.status = new_status

                if new_status == Status.CONFIRMED:
                    subscription.active = True
                    subscription.ended_at = None
                elif new_status == Status.CANCELLED:
                    subscription.active = False
                    subscription.ended_at = timezone.now()
                elif new_status == Status.PENDING:
                    subscription.active = False
                    subscription.ended_at = None

                subscription.save()

                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({
                        "success": True,
                        "new_status": subscription.get_status_display(),
                        "message": "Status updated successfully",
                    })

                messages.success(request, f"Subscription status updated to {subscription.get_status_display()}")

            except Exception as e:
                if request.headers.get("x-requested-with") == "XMLHttpRequest":
                    return JsonResponse({"success": False, "message": str(e)})
                messages.error(request, f"Error updating status: {str(e)}")




        elif action == "delete":
            try:
                service_name = subscription.service.name
                subscription.delete()
                messages.success(request, f"Subscription for {service_name} deleted successfully")
            except Exception as e:
                messages.error(request, f"Error deleting subscription: {str(e)}")

        return redirect("dashboard_service_requests")

