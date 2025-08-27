# accounts/views.py
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UserSerializer

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def current_user(request):
    """
    Return the authenticated user's info as JSON.
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
