from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MedicappUser
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

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



@csrf_exempt
@require_http_methods(["POST"])
def payback_view(request):
    try:
        payload = json.loads(request.body)
        print("📦 GitHub Webhook Payload:")
        print(json.dumps(payload, indent=4))  # pretty-print for readability

        # Respond with acknowledgment
        return JsonResponse({"message": "Payload received"}, status=200)
    except Exception as e:
        print(f"❌ Error parsing payload: {e}")
        return JsonResponse({"error": str(e)}, status=400)
