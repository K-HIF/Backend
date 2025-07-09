# users/serializers.py
from rest_framework import serializers
from .models import MedicappUser

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MedicappUser
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = MedicappUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
