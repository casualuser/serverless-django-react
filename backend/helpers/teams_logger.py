from django.conf import settings
from django.utils.log import AdminEmailHandler

import json
import requests
import os


class TeamsExceptionHandler(AdminEmailHandler):
    def emit(self, record):
        try:
            request = record.request
            subject = "%s (%s IP): %s" % (
                record.levelname,
                (
                    "internal"
                    if request.META.get("REMOTE_ADDR") in settings.INTERNAL_IPS
                    else "EXTERNAL"
                ),
                record.getMessage(),
            )
        except Exception:
            subject = "%s: %s" % (record.levelname, record.getMessage())
            request = None
        subject = self.format_subject(subject)

        connector_body = {
            "@type": "MessageCard",
            "@context": "http://schema.org/extensions",
            "themeColor": "0076D7",
            "summary": subject,
            "sections": [
                {
                    "activityTitle": subject,
                    "markdown": False,
                    "facts": [
                        {"name": "Level", "value": record.levelname},
                        {
                            "name": "Method",
                            "value": request.method if request else "No Request",
                        },
                        {
                            "name": "Path",
                            "value": request.path if request else "No Request",
                        },
                        {
                            "name": "User",
                            "value": (
                                f"{request.user.displayName} ({request.user.email})"
                                if hasattr(request, "user")
                                and request.user.is_authenticated
                                else "Anonymous User"
                            )
                            if request
                            else "No Request",
                        },
                        {"name": "Status Code", "value": record.status_code},
                        {
                            "name": "URL Params",
                            "value": json.dumps(request.GET)
                            if request
                            else "No Request",
                        },
                        {
                            "name": "Payload",
                            "value": json.dumps(request.POST)
                            if request
                            else "No Request",
                        },
                    ],
                }
            ],
        }

        requests.post(os.environ["TEAMS_WEBHOOK"], json=connector_body)
