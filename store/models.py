from django.contrib.auth.models import User
from django.db import models

from saas import models as saas_models
from xanymate import mixins


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

    def __str__(self):
        return self.collection.name


class ServiceStoreIntegration(mixins.TimeStampedMixin, mixins.UserTrackingMixin):
    service = models.ForeignKey(saas_models.Service, on_delete=models.CASCADE, related_name='integrations')
    collection = models.ForeignKey(StoreCollection, on_delete=models.CASCADE, related_name='integrations')

    def __str__(self):
        return f"{self.collection.name}->{self.service.name}"

    class Meta:
        unique_together = ("service", "collection", "created_by")


class StoreArtifactRequest(mixins.TimeStampedMixin):
    integration = models.ForeignKey(ServiceStoreIntegration, on_delete=models.CASCADE, related_name='requests')
    request = models.JSONField(default=dict)
    is_seen = models.BooleanField(default=False)

    def __str__(self):
        return self.integration.service.name
