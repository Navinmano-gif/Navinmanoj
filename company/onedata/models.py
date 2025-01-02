# from django.db import models

from django.db import models
from django.contrib.auth.models import AbstractUser

# Organization model
class Organization(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


# Role model
class Role(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


# Custom User model
class OneDataUser(AbstractUser):
    email = models.EmailField(unique=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role)
    groups = models.ManyToManyField(
        'auth.Group', 
        related_name='custom_user_groups',  # Change this to a unique name
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups')
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Provide a unique related_name
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )


class User(AbstractUser):
    # Any additional fields for your custom User model
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE)
    roles = models.ManyToManyField('Role', blank=True)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name="onedata_user_set",  # Custom related_name
        blank=True
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name="onedata_user_permissions",  # Custom related_name
        blank=True
    )
    def __str__(self):
        return self.username
