from rest_framework import permissions


class IsSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_superuser


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('core.can_manage_organization')


class IsManager(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('core.can_manage_own_organization')


class IsMember(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm('core.can_manage_member')


class IsSuperAdminOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow Super Admin or Admin of the organization to update or delete it.
    """

    def has_permission(self, request, view):
        # Allow all authenticated users to list and retrieve organizations
        if view.action in ['list', 'retrieve']:
            return True

        # Super Admin can update or delete any organization
        if request.user.is_superuser:
            return True

        # Admin can only update or delete their own organization
        if view.action in ['update', 'destroy']:
            # Assuming the user has an `organization` field and belongs to one organization
            organization = view.get_object()  # Get the current organization
            return organization.id == request.user.organization.id

        return False
    class IsSuperAdminOrAdmin(permissions.BasePermission):
    
   ## Custom permission to only allow Super Admin or Admin of the organization to update or delete roles.


     def has_permission(self, request, view):
        # Allow all authenticated users to list and retrieve roles
        if view.action in ['list', 'retrieve']:
            return True

        # Super Admin can update or delete any role
        if request.user.is_superuser:
            return True

        # Admin can only update or delete roles within their own organization
        if view.action in ['update', 'destroy']:
            organization = view.get_object().organization  # Get the organization of the role
            return organization == request.user.organization  # Check if the user belongs to the same organization

        return False

