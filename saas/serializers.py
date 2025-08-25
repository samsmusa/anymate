from rest_framework import serializers

from saas import models


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = ("id", "name", "description")