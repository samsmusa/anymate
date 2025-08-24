from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.core.paginator import Paginator
from store import models
from saas import models as saas_models


class StoreView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):

        search_query = request.GET.get("search", "")
        services = saas_models.Service.objects.all()

        if search_query:
            services = services.filter(name__icontains=search_query)

        paginator = Paginator(services.order_by("-created_at"), 12)
        page = request.GET.get("page")
        services_page = paginator.get_page(page)

        context = {
            "services": services_page,
            "search_query": search_query,
            "total_services": services.count(),
            "is_customer": not request.user.is_superuser,
        }
        return render(request, "pages/dashboard/services/store/index.html", context)


class CollectionView(LoginRequiredMixin, View):
    login_url = "login"

    def get(self, request, *args, **kwargs):

        collections_qs = (
            models.StoreCollection.objects
            .select_related("user")
            .prefetch_related("integrations__service")
        )


        if not request.user.is_superuser:
            collections_qs = collections_qs.filter(user=request.user)


        paginator = Paginator(collections_qs, 10)
        page_number = request.GET.get("page")
        collections = paginator.get_page(page_number)


        stats = {
            "total_collections": collections_qs.count(),
            "total_integrations": sum(c.integrations.count() for c in collections_qs),
            "active_users": collections_qs.values("user").distinct().count(),
        }

        return render(
            request,
            "pages/dashboard/services/store/collections.html",
            {
                "collections": collections,
                **stats
            },
        )

    def post(self, request, *args, **kwargs):
        """
        Handle collection creation
        Expecting `name` in POST
        """
        name = request.POST.get("name")
        if not name:
            messages.error(request, "Collection name is required.")
            return redirect("store_collections")

        collection = models.StoreCollection.objects.create(
            user=request.user,
            name=name
        )
        messages.success(request, f"Collection '{collection.name}' created successfully.")
        return redirect("collections")