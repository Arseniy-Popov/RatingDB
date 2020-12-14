from rest_framework import viewsets, generics, mixins, permissions

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


class UserViewSet(
    viewsets.GenericViewSet,
    mixins.CreateModelMixin,
    # mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    # mixins.DestroyModelMixin,
):
    queryset = User.objects.all()
    serializer_class = UserSerializerRead
    permission_classes = [Create(IsAny) | Read(IsAny)]

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return UserSerializerRead
        return UserSerializerWrite

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data = UserSerializerRead(
            User.objects.get(username=response.data["username"])
        ).data
        return response
