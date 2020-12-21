from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RetrieveCreateUser


urlpatterns = [
    path("", RetrieveCreateUser.as_view({"get": "retrieve", "post": "create"}))
]
