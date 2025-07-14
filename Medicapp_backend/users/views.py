from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import MedicappUser
from .models import StarCount_2
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .models import DownvoteCounter, UserDownvote, IPDownvote
from django.contrib.auth import get_user_model

User = get_user_model()
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
@require_http_methods(["POST", "GET"])
def payback_view(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            print("Received payload:", payload)  # Debugging line
            stars = payload['repository']['stargazers_count']
            print("Stars count:", stars)  # Debugging line
            # Ensure only one row exists
            star_obj, created = StarCount_2.objects.get_or_create(id=1, defaults={'count': stars})
            if not created:
                star_obj.count = stars
                star_obj.save()

            return JsonResponse({"message": "Star count saved/updated"}, status=200)

        except Exception as e:
            print(f"❌ Error parsing payload: {e}")
            return JsonResponse({"error": str(e)}, status=400)

    elif request.method == "GET":
        try:
            star_obj = StarCount_2.objects.get(id=1)
            return JsonResponse({"stars": star_obj.count})
        except StarCount_2.DoesNotExist:
            return JsonResponse({"stars": 0})
        



def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


@api_view(['GET'])
@permission_classes([AllowAny])
def get_downvotes(request):
    counter, _ = DownvoteCounter.objects.get_or_create(id=1)
    return Response({"count": counter.count})


@api_view(['POST'])
@permission_classes([AllowAny])
def post_downvote(request):
    counter, _ = DownvoteCounter.objects.get_or_create(id=1)

    if request.user.is_authenticated:
        if UserDownvote.objects.filter(user=request.user).exists():
            return Response({"detail": "You have already downvoted."}, status=status.HTTP_400_BAD_REQUEST)
        UserDownvote.objects.create(user=request.user)
    else:
        ip = get_client_ip(request)
        if IPDownvote.objects.filter(ip_address=ip).exists():
            return Response({"detail": "This IP has already downvoted."}, status=status.HTTP_400_BAD_REQUEST)
        IPDownvote.objects.create(ip_address=ip)

    counter.count += 1
    counter.save()
    return Response({"message": "Downvote successful", "count": counter.count})