# users/serializers.py
from rest_framework import serializers
from .models import InsuranceUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = InsuranceUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = InsuranceUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
