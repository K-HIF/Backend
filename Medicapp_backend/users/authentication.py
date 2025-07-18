from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import serializers

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        user = self.user

        if not user.is_active:
            raise serializers.ValidationError("User account is disabled.")

        # Restrict login for unverified non-admin users
        if user.department != 'admin' and not user.is_verified:
            raise serializers.ValidationError("Account not verified by admin.")

        
        data['user'] = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'department': user.department.name
        }

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['email'] = user.email
        token['department'] = user.department.name
        token['full_name'] = user.full_name

        return token
