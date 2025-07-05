from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Organization, User, HmiGroup, HMI
from .serializers import OrganizationSerializer, UserSerializer, HmiGroupSerializer, HMISerializer

from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import action
from rest_framework.response import Response



class OrganizationViewSet(viewsets.ModelViewSet):

        queryset = Organization.objects.all()
        serializer_class  = OrganizationSerializer
        permission_classes = [IsAuthenticated]
        @action(detail=True, methods=['get'])
        def groups(self, request, pk=None):
                """
                Returns a list of all HMI Groups for a specific Organization.
                """
                organization = self.get_object()
                group_queryset = organization.groups.all()
                serializer = HmiGroupSerializer(group_queryset, many=True)
                return Response(serializer.data)

class UserViewSet(viewsets.ModelViewSet):
        
        queryset = User.objects.all()
        serializer_class = UserSerializer

class HmiGroupViewSet(viewsets.ModelViewSet):
    serializer_class = HmiGroupSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # This filtering logic is correct and stays the same
        user = self.request.user
        if user.is_staff or user.role in [User.Role.COMPANY_X_ADMIN, User.Role.COMPANY_X_EMPLOYEE]:
            return HmiGroup.objects.all()
        return HmiGroup.objects.filter(organization=user.organization)

    def perform_create(self, serializer):
        serializer.save(organization=self.request.user.organization)

 
    def destroy(self, request, *args, **kwargs):
        hmigroup_to_delete = self.get_object()
        user = self.request.user
        
        # --- MANUAL PERMISSION CHECK ---
        can_delete = False
        # Path A: Is the user Company Staff?
        if user.role in [User.Role.COMPANY_X_ADMIN, User.Role.COMPANY_X_EMPLOYEE]:
            can_delete = True
        # Path B: Is the user a Manager of this specific group's organization?
        elif user.role == User.Role.ORG_MANAGER and user.organization == hmigroup_to_delete.organization:
            can_delete = True
        
        if not can_delete:
            raise PermissionDenied("You do not have permission to delete this group.")
        
        # If the check passes, proceed with the original deletion logic
        return super().destroy(request, *args, **kwargs)

class HmiViewSet(viewsets.ModelViewSet):
    serializer_class = HMISerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        
        user = self.request.user
        if user.is_staff or user.role in [User.Role.COMPANY_X_ADMIN, User.Role.COMPANY_X_EMPLOYEE]:
            return HMI.objects.all()
     
        return HMI.objects.filter(organization=user.organization)
        
