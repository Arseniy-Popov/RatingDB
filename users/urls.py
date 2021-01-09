from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RetrieveCreateUser, UserAdminManager

urlpatterns = [
    path("user/", RetrieveCreateUser.as_view({"get": "retrieve", "post": "create"})),
    path(
        "users/",
        UserAdminManager.as_view({"get": "list"}),
    ),
    path(
        "users/<slug:username>/",
        UserAdminManager.as_view(
            {"get": "retrieve", "patch": "partial_update", "delete": "destroy"}
        ),
    ),
]
