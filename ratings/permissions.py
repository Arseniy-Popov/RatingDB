from rest_framework import permissions


# Base Classes


class Base(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return self.read(request, view)
        return self.write(request, view)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return self.read(request, view, obj)
        return self.edit(request, view, obj)

    def read(self, *args):
        return False

    def write(self, *args):
        return False

    def edit(self, *args):
        return False


class BaseWrite(Base):
    def write(self, *args):
        return self.condition(*args)


class BaseRead(Base):
    def read(self, *args):
        return self.condition(*args)


class BaseEdit(Base):
    def edit(self, *args):
        return self.condition(*args)


# Role Mixins


class SuperMixin:
    def condition(self, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        try:
            return request.user.is_superuser
        except AttributeError:
            return False


class AdminMixin:
    def condition(self, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        try:
            return request.user.role == "admin"
        except AttributeError:
            return False


class ModeratorMixin:
    def condition(self, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        try:
            return request.user.role == "moderator"
        except AttributeError:
            return False


class OwnerMixin:
    def condition(self, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        return request.user == obj.author


class AuthenticatedMixin:
    def condition(self, *args):
        try:
            request, view, obj = args
        except ValueError:
            request, view = args
        return request.user.is_authenticated


# Write


class SuperWrite(BaseWrite, SuperMixin):
    pass


class AdminWrite(BaseWrite, AdminMixin):
    pass


class ModeratorWrite(BaseWrite, ModeratorMixin):
    pass


class OwnerWrite(BaseWrite, OwnerMixin):
    pass


class AuthenticatedWrite(BaseWrite, AuthenticatedMixin):
    pass


# Read


class AuthenticatedRead(BaseRead, AuthenticatedMixin):
    pass


class AnyRead(BaseRead):
    def condition(self, *args):
        return True


# Edit


class SuperEdit(BaseEdit, SuperMixin):
    pass


class AdminEdit(BaseEdit, AdminMixin):
    pass


class ModeratorEdit(BaseEdit, ModeratorMixin):
    pass


class OwnerEdit(BaseEdit, OwnerMixin):
    pass
