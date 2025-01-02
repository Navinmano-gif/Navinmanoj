from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoleViewSet
from .views import OrganizationViewSet, RoleViewSet, UserViewSet
from django.contrib import admin

router = DefaultRouter()
router.register(r'organizations', OrganizationViewSet)
router.register(r'roles', RoleViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter


# Create a router and register the RoleViewSet
router = DefaultRouter()
router.register(r'roles', RoleViewSet, basename='role')

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls)),  # Include the router URLs
]