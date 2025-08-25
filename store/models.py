from django.contrib.auth.models import User
from django.db import models

from saas import models as saas_models


class StoreCollection(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    vectorized_field = models.CharField(max_length=100)
    payload_schema = models.JSONField(default=dict)
    request_schema = models.JSONField(default=dict)

    def __str__(self):
        return self.name


class StoreArtifact(models.Model):
    collection = models.ForeignKey(StoreCollection, on_delete=models.CASCADE, related_name='artifacts')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artifacts')
    payload = models.JSONField(default=dict)


class ServiceStoreIntegration(models.Model):
    service = models.ForeignKey(saas_models.Service, on_delete=models.CASCADE, related_name='integrations')
    collection = models.ForeignKey(StoreCollection, on_delete=models.CASCADE, related_name='integrations')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='integrations')

    class Meta:
        unique_together = ("service", "collection", "user")

