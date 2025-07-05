from rest_framework import serializers
from .models import Organization, User, HMI, HmiGroup

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User
        fields = ['id', 'username', 'email', 'organization', 'role']

        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()

        return instance
    
class HmiGroupSerializer(serializers.ModelSerializer):
    # This is the key line
    organization = serializers.StringRelatedField()

    class Meta:
        model = HmiGroup
        fields = ['id', 'name', 'organization']

class HMISerializer(serializers.ModelSerializer):
   
    organization = serializers.StringRelatedField()
    groups = serializers.StringRelatedField(many=True, read_only=True)

    
    organization_id = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all(), source='organization', write_only=True
    )
    group_ids = serializers.PrimaryKeyRelatedField(
        queryset=HmiGroup.objects.all(), source='groups', many=True, write_only=True
    )

    class Meta:
        model = HMI
        
        fields = ['id', 'name', 'organization', 'groups', 'organization_id', 'group_ids']

    def validate(self, data):
        
      
        organization = data['organization']
        groups = data['groups']
        
        for group in groups:
            if group.organization != organization:
                raise serializers.ValidationError(
                    f"The group '{group.name}' does not belong to the selected organization '{organization.name}'."
                )
        return data