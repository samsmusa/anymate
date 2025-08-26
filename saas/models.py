from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _
from xanymate import mixins

class Status(models.IntegerChoices):
    """
    Enumeration for subscription, order, or workflow statuses.
    Stored as integers in the database, with human-readable labels.
    """
    PENDING = 1, _("Pending")
    CANCELLED = 2, _("Cancelled")
    CONFIRMED = 3, _("Confirmed")


class Service(models.Model):
    """
    Represents a SaaS service that users can subscribe to.
    `workflow` stores configuration or workflow data in JSON format.
    """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=False)
    icon = models.TextField(blank=True)
    workflow = models.JSONField(help_text="Store workflow configuration as JSON")
    config = models.JSONField(help_text="Store configuration as JSON")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Subscription(mixins.UserTrackingMixin, mixins.TimeStampedMixin):
    """
    Represents a user's subscription to a particular service.
    """
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="subscriptions")
    active = models.BooleanField(default=True)
    status = models.IntegerField(
        choices=Status.choices,
        default=Status.PENDING,
        help_text="Current subscription status"
    )
    workflow_id = models.CharField(max_length=255, blank=True, null=True, help_text="workflow ID")
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('service', 'created_by')

    def __str__(self):
        return f"{self.created_by.username} → {self.service.name}"

