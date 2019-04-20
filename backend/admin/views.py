from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser


@api_view(["POST"])
@permission_classes([IsAdminUser])
def dashboard(request):
    # A MS Graph call can be performed using received access_token
    access_token = request.data.get("accessToken")
    return Response({"status": "success"})
