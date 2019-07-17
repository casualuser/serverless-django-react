from base64 import b64decode
from ast import literal_eval
import os
import requests
import jwt
import re
from datetime import datetime as dt, timezone
import random

import logging

from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User

logger = logging.getLogger("audit")


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

    # Randomly generate a zID if coming from personal ActiveDirectory
    # because employeeId will likely be blank
    if os.environ["STAGE"] != "prod" and not user_data["employeeId"]:
        user_data["employeeId"] = random.randint(1000000, 9999999)

    zid = f'z{user_data["employeeId"]}'
    username = user_data["userPrincipalName"]
    updated_data = {
        "first_name": user_data["givenName"],
        "last_name": user_data["surname"],
        "display_name": user_data["displayName"],
        "job_title": user_data["jobTitle"],
        "is_staff": is_admin,
        "last_login": dt.now(timezone.utc),
    }

    try:
        user = User.objects.get(username=username)
        for key, value in updated_data.items():
            setattr(user, key, value)
    except User.DoesNotExist:
        # zID, username, email and public_name are only set on user creation,
        # and are not updated on users' subsequent logins
        user = User(
            zid=zid,
            username=username,
            # "mail" may not be a key in the payload when coming from
            # personal ActiveDirectory
            email=user_data["mail"] if user_data.get("mail") else username,
            **updated_data,
        )

    user.save()

    refresh = RefreshToken.for_user(user)

    logger.info(f"authentication.login", extra={"user": user.zid})

    return {
        "is_admin": user.is_staff,
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
