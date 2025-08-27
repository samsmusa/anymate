# accounts/views.py
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


class CurrentUserAPIView(APIView):
    """
    API view to return the authenticated user's info.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Get current authenticated user",
        description="Returns the details of the currently authenticated user.",
        responses=UserSerializer
    )
    def get(self, request, format=None):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
