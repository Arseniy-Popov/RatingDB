from __future__ import annotations

from rest_framework import permissions

from .roles import ConditionMetaclass


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        return view.action in self.permitted_actions and self.condition.is_true(
            request, view
        )

    def has_object_permission(self, request, view, obj):
        return view.action in self.permitted_actions and self.condition.is_true(
            request, view, obj
        )


class PermissionMetaclass(type):
    def __call__(self, condition: ConditionMetaclass) -> permissions.BasePermission:
        return type(Base)(
            f"{self.__name__}Inner",
            (Base,),
            {"permitted_actions": self.permitted_actions, "condition": condition},
        )


class List(metaclass=PermissionMetaclass):
    permitted_actions = ["list"]


class Retrieve(metaclass=PermissionMetaclass):
    permitted_actions = ["retrieve"]


class Create(metaclass=PermissionMetaclass):
    permitted_actions = ["create"]


class Update(metaclass=PermissionMetaclass):
    permitted_actions = ["update", "partial_update"]


class Delete(metaclass=PermissionMetaclass):
    permitted_actions = ["destroy"]


class Read(metaclass=PermissionMetaclass):
    permitted_actions = ["list", "retrieve"]


class Any(metaclass=PermissionMetaclass):
    permitted_actions = [
        "list",
        "retrieve",
        "create",
        "update",
        "partial_update",
        "destroy",
    ]
