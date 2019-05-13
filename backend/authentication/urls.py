from django.conf.urls import url
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    url("login/", views.login),
    url("refresh/", TokenRefreshView.as_view()),
    url("error/", views.error),
]
