from rest_framework import generics, mixins, permissions, viewsets
from rest_framework.response import Response

from ratings.permissions import Any, Create, Delete, List, Read, Retrieve, Update
from ratings.roles import (
    IsAdmin,
    IsAny,
    IsAuthenticated,
    IsAuthor,
    IsModerator,
    IsStaff,
)

from .models import User
from .serializers import (
    UserAdminManagerSerializer,
    UserSerializerRead,
    UserSerializerWrite,
)


class RetrieveCreateUser(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin
):
    queryset = User.objects.all()
    permission_classes = [Create(IsAny) | Read(IsAuthenticated)]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserSerializerRead
        return UserSerializerWrite

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        """
        Use the read serializer to populate the body of a response
        to a create action.
        """
        response = super().create(request, *args, **kwargs)
        response.data = UserSerializerRead(
            User.objects.get(username=response.data["username"]),
            context={"request": request},
        ).data
        return response


class UserAdminManager(
    viewsets.GenericViewSet, mixins.UpdateModelMixin, mixins.RetrieveModelMixin
):
    queryset = User.objects.all()
    permission_classes = [Update(IsAdmin) | Read(IsAdmin)]
    serializer_class = UserAdminManagerSerializer
    lookup_field = "username"
