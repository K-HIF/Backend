from rest_framework.views import APIView
import requests
from rest_framework.response import Response
from users.serializers import RegisterSerializer, DepartmentSerializer, ProgramSerializer, InsuranceProviderSerializer,FacilitySerializer # PatientSerializer ClaimSerializer, PharmacySerializer, PharmacyItemSerializer, NurseSerializer, LabTechnicianSerializer, PharmacistSerializer, ReceptionistSerializer, FinanceStaffSerializer, 
from .models import MedicappUser , StarCount_2, DownvoteCounter, UserDownvote, IPDownvote, Department, Program, InsuranceProvider, Facility, UpvoteCounter, UserUpvote, IPUpvote # Patient,  Claim
from django.http import JsonResponse
import json
from .utils import send_verification_email
from django.conf import settings
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
    DoctorEditSerializer,
    NurseSerializer,
    PharmacySerializer,
    LabSerializer,
    CheckoutSerializer,
    ReceptionSerializer,
    NurseEditSerializer,
    PharmacyEditSerializer,
    LabEditSerializer,
    CheckoutEditSerializer,
    ReceptionEditSerializer,
    MedicappUserSerializer,
)
from .serializers import AdminRegisterSerializer

class AdminRegisterView(APIView):
    def post(self, request):
        serializer = AdminRegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                "message": "User registered successfully.",
                "user": {
                    "email": user.email,
                    "fullName": user.full_name,
                    "department": user.department.name,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    serializer_class = DoctorEditSerializer

    def get_queryset(self):
        # Return all doctors, as we will filter by both user_id and id in the put method
        return Doctor.objects.all()

    def put(self, request, user_id, *args, **kwargs):
        print(f"Received PUT request for user_id: {user_id} with data: {request.data}")  # Debugging statement

        # Get the object to be updated
        self.object = self.get_queryset().filter(user_id=user_id).first()
        if not self.object:
            print("Doctor not found.")
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)

        print(f"Retrieved doctor object: {self.object}")  # Debugging statement

        serializer = self.get_serializer(self.object, data=request.data)

        # Validate and save the serializer
        if serializer.is_valid():
            print("Serializer is valid. Saving the doctor object.")  # Debugging statement
            serializer.save()

            if request.data.get('verification', False):  # Use get to avoid KeyError
                self.object.user.is_verified = True
                self.object.user.is_active = True
                self.object.user.save()
                print("User verified and activated.")

                # Send verification email with a password reset link instead
                send_verification_email(self.object.user.email, self.object.user.full_name)

                print("User is_verified and is_active set to True.")

            # Return a successful response with the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If the serializer is not valid, return the errors
        print(f"Serializer errors: {serializer.errors}")  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class NurseUpdateView(generics.UpdateAPIView):
    
    serializer_class = NurseEditSerializer
    def get_queryset(self):
        # Return all doctors, as we will filter by both user_id and id in the put method
        return Nurse.objects.all()

    def put(self, request, user_id, *args, **kwargs):
        print(f"Received PUT request for user_id: {user_id} with data: {request.data}")  # Debugging statement
    
        # Get the object to be updated
        self.object = self.get_queryset().filter(user_id=user_id).first()
        if not self.object:
            print("nurse not found.")
            return Response({'error': 'Nurse not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        print(f"Retrieved nurse object: {self.object}")  # Debugging statement
    
        serializer = self.get_serializer(self.object, data=request.data)
    
        # Validate and save the serializer
        if serializer.is_valid():
            print("Serializer is valid. Saving the nurse object.")  # Debugging statement
            serializer.save()
    
            if request.data.get('verification', False):  # Use get to avoid KeyError
                self.object.user.is_verified = True
                self.object.user.is_active = True
                self.object.user.save()
                print("User verified and activated.")
    
                # Send verification email with a password reset link instead
                send_verification_email(self.object.user.email, self.object.user.full_name)
    
                print("User is_verified and is_active set to True.")
    
            # Return a successful response with the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        # If the serializer is not valid, return the errors
        print(f"Serializer errors: {serializer.errors}")  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LabUpdateView(generics.UpdateAPIView):
    serializer_class = LabEditSerializer
    def get_queryset(self):
        # Return all doctors, as we will filter by both user_id and id in the put method
        return Lab.objects.all()

    def put(self, request, user_id, *args, **kwargs):
        print(f"Received PUT request for user_id: {user_id} with data: {request.data}")  # Debugging statement
    
        # Get the object to be updated
        self.object = self.get_queryset().filter(user_id=user_id).first()
        if not self.object:
            print("Labtech not found.")
            return Response({'error': 'Lab not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        print(f"Retrieved lab object: {self.object}")  # Debugging statement
    
        serializer = self.get_serializer(self.object, data=request.data)
    
        # Validate and save the serializer
        if serializer.is_valid():
            print("Serializer is valid. Saving the doctor object.")  # Debugging statement
            serializer.save()
    
            if request.data.get('verification', False):  # Use get to avoid KeyError
                self.object.user.is_verified = True
                self.object.user.is_active = True
                self.object.user.save()
                print("User verified and activated.")
    
                # Send verification email with a password reset link instead
                send_verification_email(self.object.user.email, self.object.user.full_name)
    
                print("User is_verified and is_active set to True.")
    
            # Return a successful response with the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        # If the serializer is not valid, return the errors
        print(f"Serializer errors: {serializer.errors}")  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PharmacyUpdateView(generics.UpdateAPIView):
    
    serializer_class = PharmacyEditSerializer
    def get_queryset(self):
        # Return all doctors, as we will filter by both user_id and id in the put method
        return Pharmacy.objects.all()

    def put(self, request, user_id, *args, **kwargs):
        print(f"Received PUT request for user_id: {user_id} with data: {request.data}")  # Debugging statement
    
        # Get the object to be updated
        self.object = self.get_queryset().filter(user_id=user_id).first()
        if not self.object:
            print("Pharmacist not found.")
            return Response({'error': 'Pharmacist not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        print(f"Retrieved pharmacy object: {self.object}")  # Debugging statement
    
        serializer = self.get_serializer(self.object, data=request.data)
    
        # Validate and save the serializer
        if serializer.is_valid():
            print("Serializer is valid. Saving the pharmacy object.")  # Debugging statement
            serializer.save()
    
            if request.data.get('verification', False):  # Use get to avoid KeyError
                self.object.user.is_verified = True
                self.object.user.is_active = True
                self.object.user.save()
                print("User verified and activated.")
    
                # Send verification email with a password reset link instead
                send_verification_email(self.object.user.email, self.object.user.full_name)
    
                print("User is_verified and is_active set to True.")
    
            # Return a successful response with the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        # If the serializer is not valid, return the errors
        print(f"Serializer errors: {serializer.errors}")  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckoutUpdateView(generics.UpdateAPIView):
    
    serializer_class = CheckoutEditSerializer
    def get_queryset(self):
        # Return all doctors, as we will filter by both user_id and id in the put method
        return Checkout.objects.all()

    def put(self, request, user_id, *args, **kwargs):
        print(f"Received PUT request for user_id: {user_id} with data: {request.data}")  # Debugging statement
    
        # Get the object to be updated
        self.object = self.get_queryset().filter(user_id=user_id).first()
        if not self.object:
            print("Accountant not found.")
            return Response({'error': 'Doctor not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        print(f"Retrieved Checkout object: {self.object}")  # Debugging statement
    
        serializer = self.get_serializer(self.object, data=request.data)
    
        # Validate and save the serializer
        if serializer.is_valid():
            print("Serializer is valid. Saving the Checkout object.")  # Debugging statement
            serializer.save()
    
            if request.data.get('verification', False):  # Use get to avoid KeyError
                self.object.user.is_verified = True
                self.object.user.is_active = True
                self.object.user.save()
                print("User verified and activated.")
    
                # Send verification email with a password reset link instead
                send_verification_email(self.object.user.email, self.object.user.full_name)
    
                print("User is_verified and is_active set to True.")
    
            # Return a successful response with the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        # If the serializer is not valid, return the errors
        print(f"Serializer errors: {serializer.errors}")  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ReceptionUpdateView(generics.UpdateAPIView):

    serializer_class = ReceptionEditSerializer
    def get_queryset(self):
        # Return all doctors, as we will filter by both user_id and id in the put method
        return Reception.objects.all()

    def put(self, request, user_id, *args, **kwargs):
        print(f"Received PUT request for user_id: {user_id} with data: {request.data}")  # Debugging statement
    
        # Get the object to be updated
        self.object = self.get_queryset().filter(user_id=user_id).first()
        if not self.object:
            print("Receptionist not found.")
            return Response({'error': 'Receptionist not found.'}, status=status.HTTP_404_NOT_FOUND)
    
        print(f"Retrieved doctor object: {self.object}")  # Debugging statement
    
        serializer = self.get_serializer(self.object, data=request.data)
    
        # Validate and save the serializer
        if serializer.is_valid():
            print("Serializer is valid. Saving the receptionist object.")  # Debugging statement
            serializer.save()
    
            if request.data.get('verification', False):  # Use get to avoid KeyError
                self.object.user.is_verified = True
                self.object.user.is_active = True
                self.object.user.save()
                print("User verified and activated.")
    
                # Send verification email with a password reset link instead
                send_verification_email(self.object.user.email, self.object.user.full_name)
    
                print("User is_verified and is_active set to True.")
    
            # Return a successful response with the updated data
            return Response(serializer.data, status=status.HTTP_200_OK)
    
        # If the serializer is not valid, return the errors
        print(f"Serializer errors: {serializer.errors}")  # Debugging statement
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        print("POST request received")
        print("Request path:", request.path)
        print("Request user:", request.user)
        return super().post(request, *args, **kwargs)

class RegisterUserView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        print("Register request data:", request.data) 
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User registered successfully"}, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
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

#upvotes
@api_view(['GET'])
@permission_classes([AllowAny])
def get_upvotes(request):
    counter, _ = UpvoteCounter.objects.get_or_create(id=1)
    return Response({"count": counter.count})


@api_view(['POST'])
@permission_classes([AllowAny])
def post_upvote(request):
    counter, _ = UpvoteCounter.objects.get_or_create(id=1)

    if request.user.is_authenticated:
        if UserUpvote.objects.filter(user=request.user).exists():
            return Response({"detail": "You have already upvoted."}, status=status.HTTP_400_BAD_REQUEST)
        UserUpvote.objects.create(user=request.user)
    else:
        ip = get_client_ip(request)
        if IPUpvote.objects.filter(ip_address=ip).exists():
            return Response({"detail": "This IP has already upvoted."}, status=status.HTTP_400_BAD_REQUEST)
        IPUpvote.objects.create(ip_address=ip)

    counter.count += 1
    counter.save()
    return Response({"message": "Upvote successful", "count": counter.count})

class GoogleRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('credential') or request.data.get('token')
        department = request.data.get('department')

        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        if response.status_code != 200:
            return Response({'error': 'Invalid token', 'details': response.json()}, status=status.HTTP_400_BAD_REQUEST)

        user_data = response.json()
        email = user_data.get('email')
        full_name = user_data.get('name')
        print("User data from Google:", user_data)
        print("Email:", email)
        print("Full name:", full_name)
        if not email:
            return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = RegisterSerializer(data={
            'email': email,
            'fullName': full_name,
            'department': department,
        })

        if serializer.is_valid():
            user = serializer.save()

            # Issue JWT tokens
            refresh = RefreshToken.for_user(user)

            return Response({
                'user': {
                    'email': user.email,
                    'full_name': user.fullName,
                    'department': user.department,
                },
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)

        print("Serializer errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        token = request.data.get('credential') or request.data.get('token')
        department = request.data.get('department')

        if not token:
            return Response({'error': 'No token provided'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.get(f'https://oauth2.googleapis.com/tokeninfo?id_token={token}')
        if response.status_code != 200:
            return Response({'error': 'Invalid token', 'details': response.json()}, status=status.HTTP_400_BAD_REQUEST)

        user_data = response.json()
        email = user_data.get('email')
        full_name = user_data.get('name')
        print("User data from Google:", user_data)

        if not email:
            return Response({'error': 'Email not found in token'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # ✅ Check if user already exists
            user = MedicappUser.objects.get(email=email)
            dept=Department.objects.get(name=department)
            
            if user.department_id != dept.id:
                return Response(
                    {'detail': "You are not a '" + department + "' user."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            if user.is_verified:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': {
                        'email': user.email,
                        'full_name': user.full_name,
                        'department': dept.name,
                    },
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                }, status=status.HTTP_200_OK)
            else:
                return Response(
                    {'detail': 'Account exists, but wait for admin verification.'},
                    status=status.HTTP_403_FORBIDDEN
                )

        except MedicappUser.DoesNotExist:
            if department == 'admin':
                return Response(
                    {'detail': "You cannot register as an 'admin' user."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            serializer = RegisterSerializer(data={
                'email': email,
                'fullName': full_name,
                'department': department,
            })

            if serializer.is_valid():
                user = serializer.save()  # 🔥 This actually creates the user in DB
                return Response({
                    'user': {
                        'email': user.email,
                        'full_name': user.full_name,
                        'department': user.department.name,
                    },
                    'access': None,
                    'refresh': None,
                    'detail': 'Account created. Wait for admin verification.'
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentListCreateView(generics.ListCreateAPIView):
    serializer_class = DepartmentSerializer
    
    
    def get_queryset(self):
        return Department.objects.exclude(name__iexact='admin')
     

class DepartmentRetrieveUpdateView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    def get(self, request, *args, **kwargs):
        print("GET request received")
        print("Request path:", request.path)
        print("Request user:", request.user)
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        print("PUT request received")
        print("Request data:", request.data)
        instance = self.get_object()
        print("Original Department instance:", instance)
        return super().put(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print("PATCH request received")
        print("Request data:", request.data)
        instance = self.get_object()
        print("Original Department instance:", instance)
        return super().patch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print("DELETE request received")
        instance = self.get_object()
        print("Deleting Department instance:", instance)
        return super().delete(request, *args, **kwargs)


class ProgramRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    


class InsuranceProviderListCreateView(generics.ListCreateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer
    


class InsuranceProviderRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = InsuranceProvider.objects.all()
    serializer_class = InsuranceProviderSerializer
   

class FacilityListCreateView(generics.ListCreateAPIView):
    serializer_class = FacilitySerializer
    

    def get_queryset(self):
        print(self.request.headers) 
        queryset = Facility.objects.all()
        department_id = self.request.query_params.get('department')
        if department_id:
            queryset = queryset.filter(department_id=department_id)
        return queryset


class FacilityRetrieveUpdateView(generics.RetrieveUpdateAPIView):
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer
    

class ProgramListCreateView(generics.ListCreateAPIView):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    

    


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
