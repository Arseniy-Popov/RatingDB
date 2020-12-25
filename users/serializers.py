from rest_framework import serializers

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
        
    
