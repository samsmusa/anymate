from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for Django's built-in User model with customer flag."""

    is_customer = serializers.SerializerMethodField()

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
            "is_customer",   # 👈 added field
        ]
        read_only_fields = ["id", "is_staff", "date_joined", "is_customer"]

    def get_is_customer(self, obj):
        return obj.groups.filter(name="customer").exists()

