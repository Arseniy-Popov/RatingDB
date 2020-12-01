from __future__ import annotations

from rest_framework import permissions


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        print("has permission", request, view, view.action)
        return (
            self.condition.is_true(request, view)
            and view.action in self.permitted_actions
        )

    def has_object_permission(self, request, view, obj):
        print(request, view, obj)
        return (
            self.condition.is_true(request, view, obj)
            and view.action in self.permitted_actions
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


class Edit(metaclass=PermissionMetaclass):
    permitted_actions = ["edit"]


class Delete(metaclass=PermissionMetaclass):
    permitted_actions = ["delete"]


class Read(metaclass=PermissionMetaclass):
    permitted_actions = ["list", "retrieve"]


class All(metaclass=PermissionMetaclass):
    permitted_actions = ["list", "retrieve", "create", "edit", "delete"]


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


class BaseRoleCondition(BaseCondition):
    @classmethod
    def is_true(cls, *args, **kwargs):
        request, view, obj = cls._resolve_args(*args, **kwargs)
        return getattr(request.user, cls.role)


class IsAny(BaseCondition):
    @classmethod
    def is_true(cls, *args, **kwargs):
        return True


class IsAuthenticated(BaseRoleCondition):
    role = "is_authenticated"


class IsAdmin(BaseRoleCondition):
    role = "is_admin"


class IsModerator(BaseRoleCondition):
    role = "is_moderator"


class IsOwner(BaseCondition):
    @classmethod
    def is_true(cls, *args, **kwargs):
        print(args)
        request, view, obj = cls._resolve_args(*args, **kwargs)
        return request.user == obj.author
