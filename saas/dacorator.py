from functools import wraps
from django.http import JsonResponse
from core.models import Subscription, Service


def require_subscription(service_name):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({"error": "Authentication required"}, status=401)

            try:
                service = Service.objects.get(name=service_name)
                subscribed = Subscription.objects.filter(
                    user=request.user, service=service, active=True
                ).exists()
                if not subscribed:
                    return JsonResponse({"error": "No active subscription"}, status=403)
            except Service.DoesNotExist:
                return JsonResponse({"error": "Service not found"}, status=404)

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
