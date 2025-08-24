from saas import models


def default_context(request):
    """Global context available in all templates."""
    if request.path.startswith("/dashboard/"):
        services = models.Subscription.objects.select_related("service").filter(user=request.user, status=models.Status.CONFIRMED)
        return {
            "context_subscribed_services": services,
            "support_email": "support@anymate.com",
            "is_customer": request.user.is_authenticated and request.user.groups.filter(name="customer").exists(),
        }
    return {}
