from rest_framework import viewsets, generics, mixins, permissions
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializerRead, UserSerializerWrite
from ratings.permissions import Any, Create, Delete, List, Read, Retrieve, Update
from ratings.roles import (
    IsAdmin,
    IsAny,
    IsAuthenticated,
    IsAuthor,
    IsModerator,
    IsStaff,
)


class RetrieveCreateUser(
    viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.RetrieveModelMixin
):
    queryset = User.objects.all()
    serializer_class = UserSerializerRead
    permission_classes = [Create(IsAny) | Read(IsAny)]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserSerializerRead
        return UserSerializerWrite

    def get_object(self):
        return self.request.user

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = UserSerializerRead(
            User.objects.get(username=response.data["username"])
        ).data
        return response

    def retrieve(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response("Unauthenticated")
        return super().retrieve(request, *args, **kwargs)
