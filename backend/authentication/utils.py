from base64 import b64decode
from ast import literal_eval
import os
import requests
import jwt
import re

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import make_password

from .serializers import UserSerializer
from .models import User


def decode_id_token(token):
    token_header = token.split(".")[0]
    try:
        decoded_header_bytes = b64decode(token_header)
        decoded_header = literal_eval(decoded_header_bytes.decode("utf-8"))
    except:
        return None

    kid = decoded_header["kid"]
    discovery_keys_url = os.environ.get(
        "DISCOVERY_KEYS_URL", "https://login.microsoftonline.com/common/discovery/keys"
    )
    jwks = requests.get(discovery_keys_url).json()

    for key in jwks["keys"]:
        if key["kid"] == kid:
            ms_pubkey = key["x5c"][0]

    pem_start = "-----BEGIN CERTIFICATE-----\n"
    # Create a new line every 64 characters in the public key
    # Refer to https://cryptography.io/en/latest/faq/#why-can-t-i-import-my-pem-file
    ms_pubkey = re.sub("(.{64})", "\\1\n", ms_pubkey, 0, re.DOTALL)
    pem_end = "\n-----END CERTIFICATE-----\n"

    cert_str = str.encode(pem_start + ms_pubkey + pem_end)
    cert_obj = load_pem_x509_certificate(cert_str, default_backend())
    public_key = cert_obj.public_key()

    try:
        decoded_token = jwt.decode(
            token, public_key, algorithms=["RS256"], audience=os.environ["AZURE_APP_ID"]
        )
        return decoded_token
    except:
        return None


def identify_user(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}

    user_data = requests.get(
        "https://graph.microsoft.com/beta/me/", headers=headers
    ).json()

    groups = (
        requests.post(
            "https://graph.microsoft.com/v1.0/me/getMemberGroups",
            headers=headers,
            json={"securityEnabledOnly": True},
        )
        .json()
        .get("value")
    )

    is_admin = False
    if os.environ["AZURE_ADMIN_GROUP_ID"] in groups:
        is_admin = True
    
    username = user_data["userPrincipalName"]
    user_data = {
        "zid": "z" + str(user_data["employeeId"]),
        "first_name": user_data["givenName"],
        "last_name": user_data["surname"],
        "display_name": user_data["displayName"],
        "email": user_data["mail"],
        "faculty": user_data["department"],
        "school": user_data["companyName"],
        "title": user_data["jobTitle"],
        "department": user_data["department"],
        "is_staff": is_admin,
    }

    user = None
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        serializer = UserSerializer(user, data=user_data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
    else:
        # The password is simply used to generate a JWT
        # Users cannot authenticate using this password
        # The only means for authentication are when the user comes from
        # the Azure SSO with a valid token
        password = make_password(username)
        serializer = UserSerializer(
            data={"username": username, "password": password, **user_data}
        )
        if serializer.is_valid():
            user = serializer.save()

    if user:
        auth = {"username": username, "password": username}
        return {
            "is_admin": user.is_staff,
            **TokenObtainPairSerializer(auth).validate(auth),
        }
