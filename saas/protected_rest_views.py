from django.http import Http404
from django_filters.rest_framework.backends import DjangoFilterBackend
from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from xanymate.permissions import IsAdmin, IsCustomer
from saas import models


@extend_schema(tags=["protected-services"])
class ProtectedServicesViewSet(viewsets.ModelViewSet):
    queryset = models.Service.objects.all()
    serializer_class = public_product_serializer.ProductSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_queryset(self):
        store = StoreManager.objects.select_related('vendor').filter(user=self.request.user).first()
        if store:
            return Product.objects.select_related('vendor').filter(vendor=store.vendor)
        raise Http404(
            "No Store Found"
        )

    def get_serializer_class(self):
        if self.action == 'list':
            return public_product_serializer.ProductSerializer
        else:
            return public_product_serializer.ProductDetailSerializer

    def perform_create(self, serializer):
        vendor = StoreManager.objects.select_related('vendor').get(user=self.request.user).vendor
        serializer.save(vendor=vendor, user=self.request.user)


@extend_schema(tags=["protected-product"])
class ProtectedProductReviewViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = private_product_serializer.ProductReviewSerializer
    lookup_field = 'pk'
    filter_backends = [DjangoFilterBackend]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        vendor = StoreManager.objects.select_related('vendor').get(user=self.request.user).vendor
        return ProductReview.objects.select_related('product', 'product__vendor').filter(
            user=self.request.user,
            product__id=self.kwargs['product_pk'],
            product__vendor=vendor
        )
