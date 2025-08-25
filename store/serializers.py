from rest_framework import serializers

from store import models


class StoreCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCollection
        fields = "__all__"


class StoreArtifactsSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.StoreArtifact
        fields = "__all__"
