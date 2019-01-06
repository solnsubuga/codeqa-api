from django.utils import timezone
from django.contrib.auth import authenticate

from rest_framework import serializers
from django.contrib.auth.models import User
from .identity import IdentityManager


class SignUpSerializer(serializers.ModelSerializer):
    """Serializer for signing a user
    """
    password = serializers.CharField(
        max_length=128,
        min_length=6,
        write_only=True
    )
    email = serializers.EmailField(
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate_email(self, email):
        """Validate email """

        user = User.objects.filter(email=email).first()
        if user:
            raise serializers.ValidationError('Email already in use')
        return email

    def create(self, validated_data):
        """ Create a new user"""
        return User.objects.create_user(**validated_data)


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, data):
        """validate the data and authenticate the user"""

        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if not user.is_active:
                raise serializers.ValidationError(
                    'Account is deactivated, contact support')
            identity_model = IdentityManager()
            payload = {
                'sub': user.id,
                'isStaff': user.is_staff,
                'isAdmin': user.is_superuser,
                'email': user.email,
                'username': user.username,
                'id': user.pk
            }
            user.last_login = timezone.now()
            user.save()
            return {
                'token': identity_model.encode(payload, 36000),
                'username': username
            }
        raise serializers.ValidationError('Wrong username or password')
