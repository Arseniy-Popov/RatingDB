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
        for role in cls.roles:
            try:
                if getattr(request.user, role):
                    return True
            except:
                pass
        return False


class IsAny(BaseCondition):
    @classmethod
    def is_true(cls, *args, **kwargs):
        return True


class IsAuthenticated(BaseRoleCondition):
    roles = ["is_authenticated"]


class IsAdmin(BaseRoleCondition):
    roles = ["is_admin"]


class IsModerator(BaseRoleCondition):
    roles = ["is_moderator"]


class IsStaff(BaseRoleCondition):
    roles = ["is_admin", "is_moderator"]


class IsAuthor(BaseCondition):
    @classmethod
    def is_true(cls, *args, **kwargs):
        request, view, obj = cls._resolve_args(*args, **kwargs)
        if not obj:
            return True
        return request.user == obj.author if hasattr(request, "user") else False
