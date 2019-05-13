from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import views, status
import requests
import os
import logging

from .utils import decode_id_token, identify_user

logger = logging.getLogger("msal")


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


@api_view(["POST"])
@permission_classes([AllowAny])
def error(request):
    if os.environ.get("TEAMS_WEBHOOK"):
        connector_body = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": "MSAL Error",
            "sections": [
                {
                    "activityTitle": "MSAL Error",
                    "markdown": False,
                    "facts": [
                        {"name": "Name", "value": request.data.get("name")},
                        {"name": "Code", "value": request.data.get("code")},
                        {"name": "Message", "value": request.data.get("message")},
                    ],
                }
            ],
        }
        requests.post(config("TEAMS_WEBHOOK"), json=connector_body)

    logger.error(
        request.data.get("name"),
        extra={
            "code": request.data.get("code"),
            "description": request.data.get("message"),
            "stack": request.data.get("stack"),
        },
    )

    return HttpResponse(status=204)
