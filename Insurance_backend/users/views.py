from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import InsuranceUser
from django.http import JsonResponse
import json

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("Login request data:", request.data)  # Debugging line
        user = authenticate(username=username, password=password)
        print("Authenticated user:", user)  # Debugging line
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        print("Request data:", request.data)

        if serializer.is_valid():
            print("Validated data:", serializer.validated_data)  # ✅ use this
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)  # ✅ safe after .save()
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def payback_view(request):
    if request.method == 'POST':
        try:
            payload = json.loads(request.body)
            print("Received payload:", payload)
        except json.JSONDecodeError:
            print("Invalid JSON received")
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        return JsonResponse({'message': 'Payload received', 'data': payload})
    
    return JsonResponse({'error': 'Only POST method allowed'}, status=405)