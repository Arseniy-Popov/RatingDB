from __future__ import annotations

from rest_framework import permissions

from .roles import ConditionMetaclass


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        return self._permitted_action(request, view) and self.condition.is_true(
            request, view
        )

    def has_object_permission(self, request, view, obj):
        return self._permitted_action(request, view) and self.condition.is_true(
            request, view, obj
        )

    def _permitted_action(self, request, view):
        if hasattr(view, "action"):
            permitted = view.action in self.permitted_actions
        else:
            permitted = request.method in self._method_from_action(
                self.permitted_actions
            )
        return permitted

    @staticmethod
    def _method_from_action(actions):
        action_to_method_map = {
            "list": "GET",
            "retrieve": "GET",
            "create": "POST",
            "update": "PUT",
            "partial_update": "PATCH",
            "destroy": "DELETE",
        }
        return [action_to_method_map[action] for action in actions]


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
