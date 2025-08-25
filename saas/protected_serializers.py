from django.contrib.auth.models import User
from rest_framework import serializers

from saas import models


class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django's built-in User model."""

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = ["id", "is_staff", "date_joined"]


class ProtectedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = "__all__"


class ProtectedSubscriptionSerializer(serializers.ModelSerializer):
    service = ProtectedServiceSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.Subscription
        fields = "__all__"
        read_only_fields = [
            f.name for f in models.Subscription._meta.fields
            if f.name != "status"
        ]
