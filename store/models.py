from django.contrib.auth.models import User
from django.db import models
from xanymate import mixins
from saas import models as saas_models


class StoreCollection(mixins.TimeStampedMixin, mixins.UserTrackingMixin):
    name = models.CharField(max_length=100)
    vectorized_field = models.CharField(max_length=100)
    payload_schema = models.JSONField(default=dict)
    request_schema = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class StoreArtifact(mixins.TimeStampedMixin, mixins.UserTrackingMixin):
    collection = models.ForeignKey(StoreCollection, on_delete=models.CASCADE, related_name='artifacts')
    payload = models.JSONField(default=dict)


class ServiceStoreIntegration(mixins.TimeStampedMixin, mixins.UserTrackingMixin):
    service = models.ForeignKey(saas_models.Service, on_delete=models.CASCADE, related_name='integrations')
    collection = models.ForeignKey(StoreCollection, on_delete=models.CASCADE, related_name='integrations')

    class Meta:
        unique_together = ("service", "collection", "created_by")

