from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.serializers import UserRegistrationSerializer, DoctorSerializer, PatientSerializer, DepartmentSerializer, ProgramSerializer, InsuranceProviderSerializer, ClaimSerializer, PharmacySerializer, PharmacyItemSerializer, NurseSerializer, LabTechnicianSerializer, PharmacistSerializer, ReceptionistSerializer, FinanceStaffSerializer
from .models import MedicappUser, StarCount_2, DownvoteCounter, UserDownvote, IPDownvote, Doctor, Patient, Department, Program, InsuranceProvider, Claim, Pharmacy, PharmacyItem, Nurse, LabTechnician, Pharmacist, Receptionist, FinanceStaff
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import generics

from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2

User = get_user_model()


class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print("Login request data:", request.data)
        user = authenticate(username=username, password=password)
        print("Authenticated user:", user)
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
            print("Validated data:", serializer.validated_data)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@require_http_methods(["POST", "GET"])
def payback_view(request):
    if request.method == "POST":
        try:
            payload = json.loads(request.body)
            print("Received payload:", payload)
            stars = payload['repository']['stargazers_count']
            print("Stars count:", stars)
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


# ✅ Google Login View using your custom MedicappUser
class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('credential') or request.data.get('token')
        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        strategy = load_strategy(request)
        backend = GoogleOAuth2(strategy)

        try:
            user_data = backend.user_data(token)
        except Exception as e:
            return Response({'error': 'Invalid token', 'details': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        email = user_data.get('email')
        username = email  # Use email as username

        if not email:
            return Response({'error': 'Email not found'}, status=status.HTTP_400_BAD_REQUEST)

        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'username': username,
                'is_active': True,
            }
        )

        if created:
            user.set_unusable_password()
            user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh),
            'user': {
                'email': user.email,
                'username': user.username,
            }
        }, status=status.HTTP_200_OK)


class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        queryset = Doctor.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class DoctorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class PatientListCreateView(generics.ListCreateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class PatientRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DepartmentListCreateView(generics.ListCreateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class DepartmentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class ProgramRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class InsuranceProviderListCreateView(generics.ListCreateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer


class InsuranceProviderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer


class ClaimListCreateView(generics.ListCreateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class ClaimRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer


class PharmacyListCreateView(generics.ListCreateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


class PharmacyRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer


class PharmacyItemListCreateView(generics.ListCreateAPIView):
    queryset = PharmacyItem.objects.all()
    serializer_class = PharmacyItemSerializer


class PharmacyItemRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = PharmacyItem.objects.all()
    serializer_class = PharmacyItemSerializer


class NurseListCreateView(generics.ListCreateAPIView):
    serializer_class = NurseSerializer

    def get_queryset(self):
        queryset = Nurse.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class NurseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer


class LabTechnicianListCreateView(generics.ListCreateAPIView):
    serializer_class = LabTechnicianSerializer

    def get_queryset(self):
        queryset = LabTechnician.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class LabTechnicianRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = LabTechnician.objects.all()
    serializer_class = LabTechnicianSerializer


class PharmacistListCreateView(generics.ListCreateAPIView):
    serializer_class = PharmacistSerializer

    def get_queryset(self):
        queryset = Pharmacist.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class PharmacistRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Pharmacist.objects.all()
    serializer_class = PharmacistSerializer


class ReceptionistListCreateView(generics.ListCreateAPIView):
    serializer_class = ReceptionistSerializer

    def get_queryset(self):
        queryset = Receptionist.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class ReceptionistRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Receptionist.objects.all()
    serializer_class = ReceptionistSerializer


class FinanceStaffListCreateView(generics.ListCreateAPIView):
    serializer_class = FinanceStaffSerializer

    def get_queryset(self):
        queryset = FinanceStaff.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class FinanceStaffRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = FinanceStaff.objects.all()
    serializer_class = FinanceStaffSerializer
