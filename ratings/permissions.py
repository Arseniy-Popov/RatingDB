from rest_framework import permissions


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return self.read_list(request, view) or self.read(request, view)
        return self.write(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return self.read_obj(request, view, obj) or self.read(request, view)
        return self.edit(request, view, obj)

    def read_list(self, *args):
        return False

    def read_obj(self, *args):
        return False

    def read(self, *args):
        return False

    def write(self, *args):
        return False

    def edit(self, *args):
        return False


class CheckCondition:
    def check_condition(self, condition, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        if condition == "is_owner":
            return request.user == obj.author
        elif hasattr(request.user, condition):
            return getattr(request.user, condition)
        return False


class ReadPermission(CheckCondition):
    def __init__(self, *conditions):
        self.conditions = conditions

    def read(self, *args):
        return any(
            self.check_condition(condition, *args) for condition in self.conditions
        )


class WritePermission(CheckCondition):
    def __init__(self, *conditions):
        self.conditions = conditions

    def write(self, *args):
        return any(
            self.check_condition(condition, *args) for condition in self.conditions
        )


class EditPermission(CheckCondition):
    def __init__(self, *conditions):
        self.conditions = conditions

    def edit(self, *args):
        return any(
            self.check_condition(condition, *args) for condition in self.conditions
        )
