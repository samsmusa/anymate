from django.db import models
from django_userforeignkey.models.fields import UserForeignKey


class TimeStampedMixin(models.Model):
    """Adds created_at and updated_at fields."""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UserTrackingMixin(models.Model):
    """Tracks who created and last updated the object."""
    created_by = UserForeignKey(
        auto_user_add=True,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_created")
    updated_by = UserForeignKey(
        auto_user_add=True,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True
