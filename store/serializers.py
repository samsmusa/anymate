from rest_framework import serializers

from saas import serializers as saas_serializers, models as saas_models
from store import models


class StoreCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreCollection
        fields = "__all__"


class StoreArtifactsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StoreArtifact
        fields = "__all__"


class ServiceStoreIntegrationSerializer(serializers.ModelSerializer):
    service = saas_serializers.ServiceSerializer(read_only=True)
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=saas_models.Service.objects.all(),
        source="service",
        write_only=True
    )
    collection = StoreCollectionSerializer(read_only=True)
    collection_id = serializers.PrimaryKeyRelatedField(
        queryset=models.StoreCollection.objects.all(),
        source="collection",
        write_only=True
    )

    class Meta:
        model = models.ServiceStoreIntegration
        fields = "__all__"

    def create(self, validated_data):
        collection = validated_data.get("collection")
        if collection.created_by != self.context['request'].user:
            raise serializers.ValidationError(f'you are not authorized to perform this action')
        return super().create(validated_data)


class StoreArtifactRequestSerializer(serializers.ModelSerializer):
    integration = ServiceStoreIntegrationSerializer(read_only=True)

    class Meta:
        model = models.StoreArtifactRequest
        fields = "__all__"
        read_only_fields = [
            f.name for f in models.StoreArtifactRequest._meta.fields
            if f.name != "is_seen"
        ]
