from rest_framework import permissions


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        return self._check_conditions(request, view) and view.action == self.action
        # if request.method in permissions.SAFE_METHODS:
        #     return self._read(request, view)
        # return self._write(request, view)

    def has_object_permission(self, request, view, obj):
        return self._check_conditions(request, view, obj) and view.action == self.action
        # if request.method in permissions.SAFE_METHODS:
        #     return self._read(request, view)
        # return self._edit(request, view, obj)

    def _check_conditions(self, *args):
        return any(
            self._check_condition(condition, *args) for condition in self.conditions
        )
        
    def _check_condition(self, condition, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
            obj = None
        if condition == "any":
            return True
        elif condition == "is_authenticated":
            return request.user.is_authenticated
        elif condition == "is_owner":
            return False if not obj else request.user == obj.author
        elif hasattr(request.user, condition):
            return getattr(request.user, condition)
        return False


class PermissionMetaclass(type):
    """
    Classes of this metaclass are called with an arbitrary number of
    conditions. If any of the conditions is satisfied, the action is 
    permitted (conditions are treated as if separated by `or` statements).
    
    If a passed condition doesn't match any of the following conditions,
    "any", "is_authenticated", and "is_owner", the User class object is
    checked to posses a boolean field with that name. When called, the
    class returns a subclass of rest_framework.permissions.BasePermission.
    
    To-Do: add boolean operators to conditions.
    
    Example usage:
    permission_classes = [
        Write("is_authenticated")
        | Edit("is_owner", "is_moderator")
        | Read("any")
    ]
    """
    
    def __call__(self, *conditions):
        return type(Base)(
            f"{self.__name__}Inner",
            (Base,),
            {"action": self.action, "conditions": conditions},
        )


class List(metaclass=PermissionMetaclass):
    action = "list"


class Create(metaclass=PermissionMetaclass):
    action = "create"


# class Edit(metaclass=PermissionMetaclass):
#     action = "edit"
