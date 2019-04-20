from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework import views, status
from django.contrib.auth.models import User
from django.http import Http404
import requests
import jwt

from .utils import decode_id_token, identify_user


@api_view(["POST"])
@permission_classes([AllowAny])
def login(request):
    token = request.META["HTTP_AUTHORIZATION"].split(" ")[1]
    id_token = decode_id_token(token)
    if not id_token:
        return Response(
            {"error": "Azure ID token validation failed"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    access_token = request.data.get("accessToken")
    # Identify user with the graphData from /me
    # Then get/create the user in the application database
    # Then generate their JWTs
    tokens = identify_user(access_token)

    if not tokens:
        return Response(
            {"message": "Failed to generate authentication tokens"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    return Response(tokens)
