from rest_framework import serializers
from automation import models


class AnnotationTagEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AnnotationTagEntity
        fields = "__all__"



class AuthProviderSyncHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AuthProviderSyncHistory
        fields = "__all__"


class CredentialsEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CredentialsEntity
        fields = "__all__"


class EventDestinationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventDestinations
        fields = "__all__"


class ExecutionAnnotationTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExecutionAnnotationTags
        fields = "__all__"


class ExecutionAnnotationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExecutionAnnotations
        fields = "__all__"


class ExecutionDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExecutionData
        fields = "__all__"


class ExecutionEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExecutionEntity
        fields = "__all__"


class ExecutionMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExecutionMetadata
        fields = "__all__"


class FolderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Folder
        fields = "__all__"


class FolderTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.FolderTag
        fields = "__all__"


class InsightsByPeriodSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsightsByPeriod
        fields = "__all__"


class InsightsMetadataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsightsMetadata
        fields = "__all__"


class InsightsRawSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InsightsRaw
        fields = "__all__"


class InstalledNodesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstalledNodes
        fields = "__all__"


class InstalledPackagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InstalledPackages
        fields = "__all__"


class InvalidAuthTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.InvalidAuthToken
        fields = "__all__"


class MigrationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Migrations
        fields = "__all__"


class ProcessedDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProcessedData
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Project
        fields = "__all__"


class ProjectRelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProjectRelation
        fields = "__all__"


class SettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Settings
        fields = "__all__"


class SharedCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SharedCredentials
        fields = "__all__"


class SharedWorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SharedWorkflow
        fields = "__all__"


class TagEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TagEntity
        fields = "__all__"


class TestCaseExecutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestCaseExecution
        fields = "__all__"


class TestRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestRun
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"


class UserApiKeysSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.UserApiKeys
        fields = "__all__"


class VariablesSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Variables
        fields = "__all__"


class WebhookEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WebhookEntity
        fields = "__all__"


class WorkflowEntitySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowEntity
        fields = "__all__"


class WorkflowHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowHistory
        fields = "__all__"


class WorkflowStatisticsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.WorkflowStatistics
        fields = ['id', 'count', 'latestevent', 'name', 'workflowid', 'rootcount']

    def get_id(self, obj):
        # Use a combination of workflowid and name as a virtual PK
        return f"{obj.workflowid_id}-{obj.name}"


class WorkflowsTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.WorkflowsTags
        fields = "__all__"
