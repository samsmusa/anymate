from rest_framework import serializers

from saas import models


class ProtectedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Service
        fields = "__all__"