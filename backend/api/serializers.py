"""
Serializers for API models and data.
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UploadedDataset


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class UploadedDatasetSerializer(serializers.ModelSerializer):
    """Serializer for UploadedDataset model."""
    
    class Meta:
        model = UploadedDataset
        fields = ('id', 'file_path', 'uploaded_at', 'summary_json')
        read_only_fields = ('id', 'uploaded_at')

