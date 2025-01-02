from django.contrib import admin

from django.contrib import admin
from .models import Organization, Role, User

# Register the Organization model
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    search_fields = ('name',)

# Register the Role model
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'organization')
    search_fields = ('name',)
    list_filter = ('organization',)

# Register the User model
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'organization')
    search_fields = ('username', 'email')
    list_filter = ('organization',)

# Register models to admin
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(User, UserAdmin)
