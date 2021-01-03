from rest_framework import serializers

from ratings.roles import IsAdmin, IsModerator

from .models import User


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
        """
        Populate `roles` field with list of assigned roles.
        """
        roles = [IsAdmin, IsModerator]
        return [
            role.__name__
            for role in roles
            if role.is_true(self.context["request"], None, None)
        ]


class UserAdminManagerSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "is_admin",
            "is_moderator",
        ]
        read_only_fields = ["username", "first_name", "last_name", "email"]
