from django.urls import path
from django.conf.urls import include

urlpatterns = [
    path("auth/", include("authentication.urls")),
    path("admin/", include("admin.urls")),
]
