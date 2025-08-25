from rest_framework import serializers

from saas import models


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        exclude = ["workflow", "config"]


class SubscriptionSerializer(serializers.ModelSerializer):
    service = ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=models.Service.objects.all(),
        source="service",
        write_only=True
    )

    class Meta:
        model = models.Subscription
        fields = ("id", "service", "service_id")
