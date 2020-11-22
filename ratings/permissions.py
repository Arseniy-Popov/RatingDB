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

    def check_condition(self, condition, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        if condition == "any":
            return True
        elif condition == "is_authenticated":
            return request.user.is_authenticated
        elif condition == "is_owner":
            return request.user == obj.author
        elif hasattr(request.user, condition):
            return getattr(request.user, condition)
        return False

    def check_conditions(self, *args):
        return any(
            self.check_condition(condition, *args) for condition in self.conditions
        )

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


class PermissionMetaclass(type):
    def __call__(self, *conditions):
        return type(permissions.BasePermission)(
            f"{self.__name__}Inner",
            (Base,),
            {self.action: Base.check_conditions, "conditions": conditions},
        )


class Read(metaclass=PermissionMetaclass):
    action = "read"


class Write(metaclass=PermissionMetaclass):
    action = "write"


class Edit(metaclass=PermissionMetaclass):
    action = "edit"
