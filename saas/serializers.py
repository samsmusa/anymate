from rest_framework import serializers

from saas import models


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ("id", "name", "description")


class SubscriptionSerializer(serializers.ModelSerializer):
    service = ServiceSerializer()

    class Meta:
        model = models.Subscription
        fields = ("id", "service")
