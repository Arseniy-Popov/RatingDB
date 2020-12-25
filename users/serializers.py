from rest_framework import serializers

from .models import User
from ratings.roles import IsAdmin, IsModerator


class UserSerializerWrite(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]

    def create(self, validated_data):
        """
        Override create to use the proper .create_user method.
        """
        return User.objects.create_user(**validated_data)


class UserSerializerRead(serializers.ModelSerializer):
    roles = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "roles"]

    def get_roles(self, obj):
        roles = [IsAdmin, IsModerator]
        return [
            role.__name__
            for role in roles
            if role.is_true(self.context["request"], None, None)
        ]
