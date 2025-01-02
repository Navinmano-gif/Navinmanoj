from django.test import TestCase

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Organization, Role
import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from .models import Organization, Role

class OrganizationTests(APITestCase):

    def setUp(self):
        self.superuser = get_user_model().objects.create_superuser(
            username='superadmin', password='password', email='superadmin@example.com'
        )
        self.admin = get_user_model().objects.create_user(
            username='admin', password='password', email='admin@example.com'
        )
        self.organization = Organization.objects.create(
            name='Test Organization', description='Test Description'
        )
        self.role = Role.objects.create(
            name='Admin', description='Admin role', organization=self.organization
        )
        self.admin.organization = self.organization
        self.admin.save()

    def test_create_organization_superadmin(self):
        self.client.force_authenticate(user=self.superuser)
        data = {'name': 'New Organization', 'description': 'New Description'}
        response = self.client.post('/api/organizations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_organization_admin(self):
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'Admin Organization', 'description': 'Admin Description'}
        response = self.client.post('/api/organizations/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_organization(self):
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'Updated Organization', 'description': 'Updated Description'}
        response = self.client.patch(f'/api/organizations/{self.organization.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

@pytest.fixture
def super_admin_user():
    user = get_user_model().objects.create_superuser(username="superadmin", password="password")
    return user

@pytest.fixture
def admin_user():
    user = get_user_model().objects.create_user(username="admin", password="password", is_staff=True)
    return user

@pytest.fixture
def organization():
    return Organization.objects.create(name="Org1", description="Test Organization")

@pytest.fixture
def role():
    return Role.objects.create(name="Admin", description="Admin role", organization=organization)

def test_create_organization_as_superadmin(super_admin_user):
    client = APIClient()
    client.force_authenticate(user=super_admin_user)
    response = client.post('/api/organizations/', {'name': 'New Org', 'description': 'New Organization'})
    assert response.status_code == 201


