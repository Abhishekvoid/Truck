from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, UserViewSet, HmiGroupViewSet, HmiViewSet


router = DefaultRouter()

router.register(r'organizations', OrganizationViewSet, basename='organization')
router.register(r'users', UserViewSet, basename='user')
router.register(r'hmigroups', HmiGroupViewSet, basename='hmigroup')
router.register(r'hmis', HmiViewSet, basename='hmi')

urlpatterns = [
    path('', include(router.urls)),
]

