from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, OpenApiTypes, OpenApiResponse
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from copy import deepcopy
from saas import models, serializers, filters, protected_serializers, utils
from saas.routes import ADMIN_ROUTE, CLIENT_ROUTE
from xanymate import permissions as xanym_permissions


@extend_schema(tags=["Public", "Public-services"])
class PublicServicesViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = serializers.ServiceSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ServiceFilter


class ServiceSidebarView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Private", "Protected", "service-sidebar"],
        summary="Get dynamic service sidebar",
        description="Returns a dynamic sidebar structure based on the user's subscriptions and role.",
        responses={
            200: OpenApiResponse(
                response=OpenApiTypes.OBJECT,
                description="Sidebar JSON object"
            )
        },
    )
    def get(self, request):
        sidebar = deepcopy(ADMIN_ROUTE)  # make a copy to avoid mutation issues
        attrib = "ADMIN_ROUTE"

        if request.user.groups.filter(name="customer").exists():
            sidebar = deepcopy(CLIENT_ROUTE)
            attrib = "CLIENT_ROUTE"

            subscriptions = models.Subscription.objects.filter(created_by=request.user).select_related("service")
            for subscription in subscriptions:
                route = utils.get_routes_from_app(
                    app_label=subscription.service.name,
                    attrib=attrib,
                    default=None
                )
                if route:
                    sidebar.setdefault("Manage Services", {}).setdefault("children", []).append(route)

        elif request.user.is_superuser:
            services = models.Service.objects.all()
            for service in services:
                route = utils.get_routes_from_app(service.name.lower(), attrib, None)
                if route:
                    sidebar.setdefault("Manage Services", {}).setdefault("children", []).append(route)

        return Response(sidebar)


@extend_schema(tags=["Private", "Private-service-subscriptions"])
class PrivateServiceSubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'put', 'patch', "post")
    queryset = models.Subscription.objects.all()
    serializer_class = serializers.SubscriptionSerializer
    lookup_field = 'pk'
    permission_classes = [xanym_permissions.IsCustomer]
    filter_backends = [DjangoFilterBackend]

    # filterset_class = filters.ServiceFilter

    def get_queryset(self):
        return models.Subscription.objects.filter(created_by=self.request.user)


@extend_schema(tags=["Protected", "Protected-services"])
class ProtectedServicesViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'put', 'patch')
    queryset = models.Service.objects.all()
    serializer_class = protected_serializers.ProtectedServiceSerializer
    permission_classes = [xanym_permissions.IsAdmin]
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ServiceFilter


@extend_schema(tags=["Protected-service-subscriptions"])
class ProtectedServiceSubscriptionViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'put', 'patch', "delete")
    queryset = models.Subscription.objects.all()
    serializer_class = protected_serializers.ProtectedSubscriptionSerializer
    lookup_field = 'pk'
    permission_classes = [xanym_permissions.IsAdmin]
    filter_backends = [DjangoFilterBackend]
