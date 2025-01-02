from rest_framework import serializers
from .models import Organization, Role, OneDataUser

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class OrganizationSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    roles = RoleSerializer(many=True, read_only=True)
    organization = OrganizationSerializer(read_only=True)

    class Meta:
        model = OneDataUser
        fields = ['id', 'username', 'email', 'organization', 'roles']
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'description', 'organization']
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneDataUser  # Use User if you're using Django's default User model
        fields = ['id', 'username', 'email', 'organization', 'roles'] 
