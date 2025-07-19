from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import RegisterSerializer, DepartmentSerializer, ProgramSerializer, InsuranceProviderSerializer,FacilitySerializer # PatientSerializer ClaimSerializer, PharmacySerializer, PharmacyItemSerializer, NurseSerializer, LabTechnicianSerializer, PharmacistSerializer, ReceptionistSerializer, FinanceStaffSerializer, 
from .models import MedicappUser , StarCount_2, DownvoteCounter, UserDownvote, IPDownvote, Department, Program, InsuranceProvider, Facility#, Doctor, Patient,  Claim, Pharmacy, PharmacyItem, Nurse, LabTechnician, Pharmacist, Receptionist, FinanceStaff, Facility
from django.http import JsonResponse
import json
from django.db.models import Value 
from rest_framework_simplejwt.tokens import RefreshToken
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework import generics
from django.contrib.auth import authenticate
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from rest_framework import status, permissions
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenRefreshView
from users.authentication import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated
from .models import Doctor, Nurse, Pharmacy, Lab, Checkout, Reception, MedicappUser
from rest_framework import generics
from rest_framework.response import Response
from .models import Department, Doctor, Nurse, Pharmacy, Lab, Checkout, Reception
from .serializers import (
    DepartmentSerializer,
    DoctorSerializer,
    NurseSerializer,
    PharmacySerializer,
    LabSerializer,
    CheckoutSerializer,
    ReceptionSerializer,
    MedicappUserSerializer,
)

class UsersInDepartmentView(generics.ListAPIView):
    print("UsersInDepartmentView called")  # Debugging line
    serializer_class = MedicappUserSerializer
    print("Serializer class set to MedicappUserSerializer")  # Debugging line
    def get_queryset(self):
        print("get_queryset called")  # Debugging line
        department_id = self.kwargs['department_id']
        print(f"Fetching users for department ID: {department_id}")  # Debugging line
        return MedicappUser.objects.filter(department_id=department_id)
    
class DepartmentListView(generics.ListAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def get(self, request, *args, **kwargs):
        print("Fetching doctors...")
        try:
            response = super().get(request, *args, **kwargs)
            print("Doctors fetched successfully.")
            print("Response data:", response.data)  # Print the response data
            return response
        except Exception as e:
            print("Error fetching doctors:", str(e))  # Print any errors
            return Response({"error": "An error occurred"}, status=500)

class NurseListView(generics.ListAPIView):
    queryset = Nurse.objects.select_related('user').all()
    serializer_class = NurseSerializer

    def get(self, request, *args, **kwargs):
        print("Fetching nurses...")
        try:
            response = super().get(request, *args, **kwargs)
            print("Nurses fetched successfully.")
            print("Response data:", response.data)  # Print the response data
            return response
        except Exception as e:
            print("Error fetching doctors:", str(e))  # Print any errors
            return Response({"error": "An error occurred"}, status=500)

class PharmacyListView(generics.ListAPIView):
    queryset = Pharmacy.objects.select_related('user').all()
    serializer_class = PharmacySerializer

    #print ("Fetching pharmacies...")
    def get(self, request, *args, **kwargs):
        print("Fetching pharmacies...")
        try:
            response = super().get(request, *args, **kwargs)
            print("Pharmacies fetched successfully.")
            print("Response data:", response.data)  # Print the response data
            return response
        except Exception as e:
            print("Error fetching pharmacies:", str(e))

            return Response({"error": "An error occurred"}, status=500)
        

class LabListView(generics.ListAPIView):
    queryset = Lab.objects.select_related('user').all()
    serializer_class = LabSerializer

    def get(self, request, *args, **kwargs):
        print("Fetching labs...")
        try:
            response = super().get(request, *args, **kwargs)
            print("Labs fetched successfully.")
            print("Response data:", response.data)  # Print the response data
            return response
        except Exception as e:
            print("Error fetching labs:", str(e))
            return Response({"error": "An error occurred"}, status=500)
        


class ReceptionListView(generics.ListAPIView):
    queryset = Reception.objects.select_related('user').all()
    serializer_class = ReceptionSerializer

    def get(self, request, *args, **kwargs):
        print("Fetching receptions...")
        try:
            response = super().get(request, *args, **kwargs)
            print("Receptions fetched successfully.")
            print("Response data:", response.data)  # Print the response data
            return response
        except Exception as e:
            print("Error fetching receptions:", str(e))
            return Response({"error": "An error occurred"}, status=500) 

class CheckoutListView(generics.ListAPIView):
    queryset = Checkout.objects.select_related('user').all()
    serializer_class = CheckoutSerializer
    def get(self, request, *args, **kwargs):
        print("Fetching checkouts...")
        try:
            response = super().get(request, *args, **kwargs)
            print("Checkouts fetched successfully.")
            print("Response data:", response.data)  # Print the response data
            return response
        except Exception as e:
            print("Error fetching checkouts:", str(e))
            return Response({"error": "An error occurred"}, status=500) 
        

class DoctorCreateView(generics.CreateAPIView):
    serializer_class = DoctorSerializer

class NurseCreateView(generics.CreateAPIView):
    serializer_class = NurseSerializer

class PharmacyCreateView(generics.CreateAPIView):
    serializer_class = PharmacySerializer

class LabCreateView(generics.CreateAPIView):
    serializer_class = LabSerializer

class CheckoutCreateView(generics.CreateAPIView):
    serializer_class = CheckoutSerializer

class ReceptionCreateView(generics.CreateAPIView):
    serializer_class = ReceptionSerializer



class DoctorUpdateView(generics.UpdateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class NurseUpdateView(generics.UpdateAPIView):
    queryset = Nurse.objects.all()
    serializer_class = NurseSerializer

class LabUpdateView(generics.UpdateAPIView):
    queryset = Lab.objects.all()
    serializer_class = LabSerializer

class PharmacyUpdateView(generics.UpdateAPIView):
    queryset = Pharmacy.objects.all()
    serializer_class = PharmacySerializer

class CheckoutUpdateView(generics.UpdateAPIView):
    queryset = Checkout.objects.all()
    serializer_class = CheckoutSerializer

class ReceptionUpdateView(generics.UpdateAPIView):
    queryset = Reception.objects.all()
    serializer_class = ReceptionSerializer

   
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(APIView):
    def post(self, request):
        print("Register request data:", request.data) 
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveUserView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, user_id):
        try:
            user = MedicappUser.objects.get(id=user_id)
            if user.is_verified:
                return Response({"detail": "User already verified."}, status=400)

            temp_password = get_random_string(10)
            user.set_password(temp_password)
            user.is_verified = True
            user.is_active = True
            user.save()

            send_mail(
                "Your MedicApp Account Approved",
                f"Email: {user.email}\nPassword: {temp_password}",
                "admin@medicapp.com",
                [user.email],
            )

            return Response({"message": "User verified and credentials sent."})
        except MedicappUser.DoesNotExist:
            return Response({"error": "User not found"}, status=404)



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


class DepartmentListCreateView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    permission_classes = [IsAuthenticated] 
    
    def get_queryset(self):
        return Department.objects.exclude(name__iexact='admin')
     

class DepartmentRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer


class ProgramRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated] 


class InsuranceProviderListCreateView(generics.ListCreateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer
    permission_classes = [IsAuthenticated] 


class InsuranceProviderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer
    permission_classes = [IsAuthenticated] 

class FacilityListCreateView(generics.ListCreateAPIView):
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated] 

    def get_queryset(self):
        queryset = Facility.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class FacilityRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    permission_classes = [IsAuthenticated] 

class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        print("⚠️ Raw request data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            print("✅ Serializer is valid:", serializer.validated_data)
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("❌ Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#class NurseListCreateView(generics.ListCreateAPIView):
#    serializer_class = NurseSerializer
#
#    def get_queryset(self):
#        queryset = Nurse.objects.all()
#        department_id = self.request.query_params.get('department')
#        if department_id:
#            queryset = queryset.filter(department_id=department_id)
#        return queryset
#
#
#class NurseRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Nurse.objects.all()
#    serializer_class = NurseSerializer
#
#    
#class DoctorListCreateView(generics.ListCreateAPIView):
#    serializer_class = DoctorSerializer
#
#    def get_queryset(self):
#        queryset = Doctor.objects.all()
#        department_id = self.request.query_params.get('department')
#        if department_id:
#            queryset = queryset.filter(department_id=department_id)
#        return queryset
#
#
#class DoctorRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Doctor.objects.all()
#    serializer_class = DoctorSerializer
#
#
#class PatientListCreateView(generics.ListCreateAPIView):
#    queryset = Patient.objects.all()
#    serializer_class = PatientSerializer
#
#
#class PatientRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Patient.objects.all()
#    serializer_class = PatientSerializer
#
#
#class DepartmentListCreateView(generics.ListCreateAPIView):
#    queryset = Department.objects.all()
#    serializer_class = DepartmentSerializer
#
#
#class DepartmentRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Department.objects.all()
#    serializer_class = DepartmentSerializer
#
#


#class ClaimListCreateView(generics.ListCreateAPIView):
#    queryset = Claim.objects.all()
#    serializer_class = ClaimSerializer
#
#
#class ClaimRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Claim.objects.all()
#    serializer_class = ClaimSerializer
#
#
#class PharmacyListCreateView(generics.ListCreateAPIView):
#    queryset = Pharmacy.objects.all()
#    serializer_class = PharmacySerializer
#
#
#class PharmacyRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Pharmacy.objects.all()
#    serializer_class = PharmacySerializer
#
#
#class PharmacyItemListCreateView(generics.ListCreateAPIView):
#    queryset = PharmacyItem.objects.all()
#    serializer_class = PharmacyItemSerializer
#
#
#class PharmacyItemRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = PharmacyItem.objects.all()
#    serializer_class = PharmacyItemSerializer
#
#

#
#
#class LabTechnicianListCreateView(generics.ListCreateAPIView):
#    serializer_class = LabTechnicianSerializer
#
#    def get_queryset(self):
#        queryset = LabTechnician.objects.all()
#        department_id = self.request.query_params.get('department')
#        if department_id:
#            queryset = queryset.filter(department_id=department_id)
#        return queryset
#
#
#class LabTechnicianRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = LabTechnician.objects.all()
#    serializer_class = LabTechnicianSerializer
#
#
#class PharmacistListCreateView(generics.ListCreateAPIView):
#    serializer_class = PharmacistSerializer
#
#    def get_queryset(self):
#        queryset = Pharmacist.objects.all()
#        department_id = self.request.query_params.get('department')
#        if department_id:
#            queryset = queryset.filter(department_id=department_id)
#        return queryset
#
#
#class PharmacistRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Pharmacist.objects.all()
#    serializer_class = PharmacistSerializer
#
#
#class ReceptionistListCreateView(generics.ListCreateAPIView):
#    serializer_class = ReceptionistSerializer
#
#    def get_queryset(self):
#        queryset = Receptionist.objects.all()
#        department_id = self.request.query_params.get('department')
#        if department_id:
#            queryset = queryset.filter(department_id=department_id)
#        return queryset
#
#
#class ReceptionistRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = Receptionist.objects.all()
#    serializer_class = ReceptionistSerializer
#
#
#class FinanceStaffListCreateView(generics.ListCreateAPIView):
#    serializer_class = FinanceStaffSerializer
#
#    def get_queryset(self):
#        queryset = FinanceStaff.objects.all()
#        department_id = self.request.query_params.get('department')
#        if department_id:
#            queryset = queryset.filter(department_id=department_id)
#        return queryset
#
#
#class FinanceStaffRetrieveUpdateView(generics.RetrieveUpdateAPIView):
#    queryset = FinanceStaff.objects.all()
#    serializer_class = FinanceStaffSerializer
#
#
