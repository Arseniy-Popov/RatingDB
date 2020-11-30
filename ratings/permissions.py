from __future__ import annotations

from rest_framework import permissions


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        return self.condition.is_true(request, view) and view.action == self.action

    def has_object_permission(self, request, view, obj):
        return self.condition.is_true(request, view, obj) and view.action == self.action


class PermissionMetaclass(type):
    def __call__(self, condition: ConditionMetaclass) -> permissions.BasePermission:
        return type(Base)(
            f"{self.__name__}Inner",
            (Base,),
            {"action": self.action, "condition": condition},
        )


class List(metaclass=PermissionMetaclass):
    action = "list"


class Create(metaclass=PermissionMetaclass):
    action = "create"


class Edit(metaclass=PermissionMetaclass):
    action = "edit"


class OperatorMixin:
    def __or__(self, other):
        return OperandHolder(OR, self, other)

    def __and__(self, other):
        return OperandHolder(AND, self, other)


class OR:
    def __init__(self, operand_1, operand_2):
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def is_true(self, *args, **kwargs):
        return self.operand_1.is_true(*args, **kwargs) or self.operand_2.is_true(
            *args, **kwargs
        )


class AND:
    def __init__(self, operand_1, operand_2):
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def is_true(self, *args, **kwargs):
        return self.operand_1.is_true(*args, **kwargs) and self.operand_2.is_true(
            *args, **kwargs
        )


class OperandHolder(OperatorMixin):
    def __init__(self, operator, operand_1, operand_2):
        self.operator = operator
        self.operand_1 = operand_1
        self.operand_2 = operand_2

    def is_true(self, *args, **kwargs):
        return self.operator(self.operand_1, self.operand_2).is_true(*args, **kwargs)


class ConditionMetaclass(OperatorMixin, type):
    pass


class BaseCondition(metaclass=ConditionMetaclass):
    @staticmethod
    def _resolve_args(*args, **kwargs):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
            obj = None
        return request, view, obj


class IsAuthenticated(BaseCondition):
    @staticmethod
    def is_true(*args, **kwargs):
        request, view, obj = self._resolve_args(*args, **kwargs)
        return request.user.is_authenticated


class IsAdmin(BaseCondition):
    @staticmethod
    def is_true(*args, **kwargs):
        request, view, obj = self._resolve_args(*args, **kwargs)
        return request.user.is_admin


class IsModerator(BaseCondition):
    @staticmethod
    def is_true(*args, **kwargs):
        request, view, obj = self._resolve_args(*args, **kwargs)
        return request.user.is_moderator
