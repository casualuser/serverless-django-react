import os
import sys
from datetime import timedelta
from boto3 import Session
import logging

SECRET_KEY = os.environ["SECRET_KEY"]

DEBUG = os.environ.get("DJANGO_DEBUG") == "true"

if os.environ.get("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django_mysql",
    "rest_framework",
    "corsheaders",
    "authentication",
    "admin",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

AUTH_USER_MODEL = "authentication.User"

ROOT_URLCONF = "app.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "app.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "HOST": os.environ["DB_HOST"],
        "PORT": int(os.environ["DB_PORT"]),
        "NAME": os.environ["DB_NAME"],
        "USER": os.environ["DB_USER"],
        "PASSWORD": os.environ["DB_PASSWORD"],
        "OPTIONS": {
            "charset": "utf8mb4",
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = os.environ.get("TIME_ZONE", "UTC")
USE_I18N = True
USE_L10N = True
USE_TZ = True

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "EXCEPTION_HANDLER": "helpers.exception_handler.JSONExceptionHandler",
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=1),
    "REFRESH_TOKEN_LIFETIME": timedelta(hours=12),
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(levelname)s %(asctime)s (%(name)s) %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
        "json": {"()": "json_log_formatter.JSONFormatter"},
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "standard",
        },
        "json_console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
            "formatter": "json",
        },
    },
    "loggers": {
        "django": {"level": "INFO", "handlers": ["console"], "propagate": False},
        "msal": {"level": "INFO", "handlers": [], "propagate": False},
        "audit": {"level": "INFO", "handlers": ["json_console"], "propagate": False},
    },
}

if os.environ.get("TEAMS_WEBHOOK"):
    LOGGING["handlers"]["teams"] = {
        "level": "WARNING",
        "class": "helpers.teams_logger.TeamsExceptionHandler",
    }
    LOGGING["loggers"]["django"]["handlers"].append("teams")

if os.environ["STAGE"] != "dev":
    session = {"region_name": os.environ.get("AWS_REGION", "ap-southeast-2")}
    if os.environ.get("AWS_PROFILE"):
        session["profile_name"] = os.environ.get("AWS_PROFILE")

    cloudwatch = {
        "level": "INFO",
        "class": "watchtower.CloudWatchLogHandler",
        "boto3_session": Session(**session),
        "log_group": os.environ["CLOUDWATCH_LOG_GROUP"],
        "use_queues": False,  # Queueing does not work within AWS Lambda execution environment
    }

    LOGGING["handlers"]["watchtower"] = {
        **cloudwatch,
        "formatter": "standard",
        "stream_name": "watchtower",
    }
    LOGGING["loggers"]["django"]["handlers"].append("watchtower")

    LOGGING["handlers"]["msal_handler"] = {
        **cloudwatch,
        "formatter": "json",
        "stream_name": "MSAL",
    }
    LOGGING["loggers"]["msal"]["handlers"].append("msal_handler")

    LOGGING["handlers"]["audit"] = {
        **cloudwatch,
        "formatter": "json",
        "stream_name": "audit",
    }
    LOGGING["loggers"]["audit"]["handlers"].append("audit")


if os.environ["CORS_WHITELIST"]:
    CORS_ORIGIN_WHITELIST = os.environ["CORS_WHITELIST"].split(",")
else:
    logging.warn("CORS_WHITELIST not provided. Defaulting to CORS_ORIGIN_ALLOW_ALL.")
    CORS_ORIGIN_ALLOW_ALL = True
