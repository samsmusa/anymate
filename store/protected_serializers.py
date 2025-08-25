from rest_framework import serializers

from store import models
from xanymate.serializers import UserSerializer


class ProtectedStoreCollectionSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = models.StoreCollection
        fields = "__all__"

class ProtectedStoreArtifactSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    class Meta:
        model = models.StoreArtifact
        fields = "__all__"