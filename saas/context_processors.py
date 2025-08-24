from saas import models, utils


def default_context(request):
    """Global context available in all templates."""
    print(utils.get_routes_from_app("facebook"))
    if request.path.startswith("/dashboard/"):
        is_customer = request.user.is_authenticated and request.user.groups.filter(name="customer").exists()
        if is_customer:
            routes_key = "CLIENT_ROUTE"
        else:
            routes_key = "ADMIN_ROUTE"
        services_qs = models.Service.objects.all()

        if not request.user.is_superuser:
            subscribed_service_ids = models.Subscription.objects.filter(
                user=request.user,
                status=models.Status.CONFIRMED
            ).values_list("service_id", flat=True)
            services_qs = services_qs.filter(id__in=subscribed_service_ids)

        services = list(services_qs)
        for service in services:
            print(service.name.lower(), utils.get_routes_from_app(service.name.lower()))
            service.routes = utils.get_routes_from_app(service.name.lower())[routes_key]

        print(services)

        return {
            "context_subscribed_services": services,
            "support_email": "support@anymate.com",
            "is_customer": is_customer,
        }

    return {}
