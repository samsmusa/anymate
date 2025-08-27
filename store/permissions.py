from rest_framework.permissions import BasePermission, SAFE_METHODS




class IsSubscriptionOwner(BasePermission):
    """
    Object-level permission to allow only owners to edit/delete.
    Assumes the model instance has a `created_by` attribute.
    """

    def has_object_permission(self, request, view, obj):
        return obj.integration.created_by == request.user


