from rest_framework import serializers

from saas import models
from xanymate.serializers import UserSerializer


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
