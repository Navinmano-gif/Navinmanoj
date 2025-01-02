from rest_framework import viewsets,permissions
from .models import Organization, Role, OneDataUser
from .models import Organization
from .serializers import OrganizationSerializer
from .permissions import IsSuperAdminOrAdmin
from .models import Role, Organization
from .serializers import RoleSerializer
from .serializers import OrganizationSerializer, RoleSerializer, UserSerializer
from .permissions import IsSuperAdmin, IsAdmin, IsManager, IsMember
from rest_framework.decorators import action

from rest_framework.response import Response
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Role, Organization
from .serializers import RoleSerializer
from .permissions import IsSuperAdminOrAdmin


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            if self.request.user.is_superuser:
                return [IsSuperAdmin()]
            return [IsAdmin()]
        return [permissions.AllowAny()]

    @action(detail=True, methods=['get'])
    def roles(self, request, pk=None):
        organization = self.get_object()
        roles = organization.role_set.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            if self.request.user.is_superuser:
                return [IsSuperAdmin()]
            return [IsAdmin()]
        return [permissions.AllowAny()]


class UserViewSet(viewsets.ModelViewSet):
    queryset = OneDataUser.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'destroy']:
            if self.request.user.is_superuser:
                return [IsSuperAdmin()]
            return [IsAdmin()]
        return [permissions.AllowAny()]
    

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

    def get_permissions(self):
        """
        Define permissions based on the action.
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated()]  # Admin/SuperAdmin can create organizations
        elif self.action == 'destroy':
            return [IsSuperAdminOrAdmin()]  # Only SuperAdmin and Admin of the organization can delete
        elif self.action == 'update':
            return [IsSuperAdminOrAdmin()]  # Only SuperAdmin and Admin of the organization can update
        return [permissions.IsAuthenticated()]  # All users can list and retrieve organizations

    def perform_create(self, serializer):
        """
        Custom perform_create to set the creator's organization automatically.
        """
        user = self.request.user
        serializer.save(created_by=user)  # Assuming you want to track who created the organization


    def get_queryset(self):
        """
        Limit organizations based on the user's role (Super Admin, Admin, etc.).
        """
        user = self.request.user
        if user.is_superuser:
            return Organization.objects.all()  # Super Admin can see all organizations
        return Organization.objects.filter(id=user.organization_id)
from rest_framework import viewsets, permissions
from rest_framework.response import Response
  # Custom permission class

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        Define permissions based on the action.
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated()]  # Admin or Super Admin can create roles
        elif self.action == 'destroy':
            return [IsSuperAdminOrAdmin()]  # Only Super Admin or Admin of the organization can delete
        elif self.action == 'update':
            return [IsSuperAdminOrAdmin()]  # Only Super Admin or Admin of the organization can update
        return [permissions.IsAuthenticated()]  # All users can list and retrieve roles

    def get_queryset(self):
        """
        Limit roles based on the user's organization.
        """
        user = self.request.user
        if user.is_superuser:
            return Role.objects.all()  # Super Admin can see all roles
        return Role.objects.filter(organization=user.organization)  # Admin can only see roles in their own organization

    def perform_create(self, serializer):
        """
        Assign the current organization when creating a role.
        """
        user = self.request.user
        # organization = user.organization  # Assuming the user has an `organization` field
        serializer.save()  # Set the organization for the role
  # Custom permission class

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

    def get_permissions(self):
        """
        Define permissions based on the action.
        """
        if self.action == 'create':
            return [permissions.IsAuthenticated()]  # Admin or Super Admin can create roles
        elif self.action == 'destroy':
            return [IsSuperAdminOrAdmin()]  # Only Super Admin or Admin of the organization can delete
        elif self.action == 'update':
            return [IsSuperAdminOrAdmin()]  # Only Super Admin or Admin of the organization can update
        return [permissions.IsAuthenticated()]  # All users can list and retrieve roles

    def get_queryset(self):
        
        user = self.request.user
        if user.is_superuser:
            return Role.objects.all()  # Super Admin can see all roles
        return Role.objects.filter(organization=user.organization)  # Admin can only see roles in their own organization

    def perform_create(self, serializer):
        """
        Assign the current organization when creating a role.
        """
        user = self.request.user
        # organization = user.organization  # Assuming the user has an `organization` field
        # serializer.save(organization=organization)
class UserViewSet(viewsets.ModelViewSet):
    queryset = OneDataUser.objects.all()  
    serializer_class = UserSerializer

    def get_permissions(self):
       
        if self.action == 'create':
            return [permissions.IsAuthenticated()]  # Admin/Super Admin can create users
        elif self.action == 'destroy':
            return [IsSuperAdminOrAdmin()]  # Only Super Admin or Admin can delete users
        elif self.action == 'update':
            return [IsSuperAdminOrAdmin()]  # Only Super Admin or Admin can update user info
        return [permissions.IsAuthenticated()]  # All users can list and retrieve users

    def get_queryset(self):
       
        user = self.request.user
        if user.is_superuser:
            return user.objects.all()  # Super Admin can see all users
        if user.organization:
            return user.objects.filter(organization=user.organization)  # Admins can only see users in their org
        return user.objects.none()  # Members only see their own user

    def perform_create(self, serializer):
        
        user = self.request.user
        serializer.save()

class OrganizationViewSet(viewsets.ModelViewSet):
       queryset = Organization.objects.all()
       serializer_class = OrganizationSerializer



# 23c9027c259b011cc1011c5085352633ea5bbe34