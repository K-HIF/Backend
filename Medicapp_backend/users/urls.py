# import necessary modules
# import JsonResponse
from django.http import JsonResponse
from django.urls import path
from .views import RegisterUserView, ApproveUserView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import DepartmentListCreateView, DepartmentRetrieveUpdateView
from . import views
from .views import (
    DepartmentListView,
    DoctorListView,
    NurseListView,
    PharmacyListView,
    DoctorCreateView,
    NurseCreateView,
    DoctorUpdateView,
    NurseUpdateView,
    PharmacyCreateView,
    PharmacyUpdateView,
    LabListView,
    LabCreateView,
    LabUpdateView,
    ReceptionListView,
    ReceptionCreateView,
    ReceptionUpdateView,
    CheckoutListView,
    CheckoutCreateView, 
    CheckoutUpdateView
    
)
from .views import payback_view,GoogleLoginView


def health_check(request):
    return JsonResponse({'status': 'ok'})
#from .views import NurseListCreateView, NurseRetrieveUpdateView

urlpatterns = [
    path('register/', RegisterUserView.as_view()),
    path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('approve/<int:user_id>/', ApproveUserView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateView.as_view(), name='department-detail'),

    # stars and downvotes
    path("health/", health_check),
    path('stars/', payback_view, name='payback'),
    path('downvotes/', views.get_downvotes),
    path('downvote/', views.post_downvote),

    #Staff URLs
    path('departments/', DepartmentListView.as_view(), name='department-list'),
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('nurses/', NurseListView.as_view(), name='nurse-list'),
    path('pharmacies/', PharmacyListView.as_view(), name='pharmacy-list'),
    path('lab/', LabListView.as_view(), name='pharmacy-list'),
    path('reception/', ReceptionListView.as_view(), name='pharmacy-list'),
    path('checkout/', CheckoutListView.as_view(), name='pharmacy-list'),
    
    path('doctors/create/', DoctorCreateView.as_view(), name='doctor-create'),
    path('nurses/create/', NurseCreateView.as_view(), name='nurse-create'),
    
    path('doctors/<int:pk>/', DoctorUpdateView.as_view(), name='doctor-update'),
    path('nurses/<int:pk>/', NurseUpdateView.as_view(), name='nurse-update'),

    path('pharmacy/create/', PharmacyCreateView.as_view(), name='doctor-create'),
    path('lab/create/', LabCreateView.as_view(), name='nurse-create'),
    
    path('pharmacy/<int:pk>/', PharmacyUpdateView.as_view(), name='doctor-update'),
    path('lab/<int:pk>/', LabUpdateView.as_view(), name='nurse-update'),

    path('reception/create/', ReceptionCreateView.as_view(), name='doctor-create'),
    path('checkout/create/', CheckoutCreateView.as_view(), name='nurse-create'),
    
    path('reception/<int:pk>/', ReceptionUpdateView.as_view(), name='doctor-update'),
    path('checkout/<int:pk>/', CheckoutUpdateView.as_view(), name='nurse-update'),

    
    
]




#from django.urls import path
#from .views import RegisterUserView, LoginView
#from django.http import JsonResponse

#from .views import DoctorListCreateView, DoctorRetrieveUpdateView
#from .views import PatientListCreateView, PatientRetrieveUpdateView
#from 
#from .views import ProgramListCreateView, ProgramRetrieveUpdateView
#from .views import InsuranceProviderListCreateView, InsuranceProviderRetrieveUpdateView
#from .views import ClaimListCreateView, ClaimRetrieveUpdateView
#from .views import PharmacyListCreateView, PharmacyRetrieveUpdateView
#from .views import PharmacyItemListCreateView, PharmacyItemRetrieveUpdateView
#
#from .views import LabTechnicianListCreateView, LabTechnicianRetrieveUpdateView
#from .views import PharmacistListCreateView, PharmacistRetrieveUpdateView
#from .views import ReceptionistListCreateView, ReceptionistRetrieveUpdateView
#from .views import FinanceStaffListCreateView, FinanceStaffRetrieveUpdateView
#from .views import FacilityListCreateView, FacilityRetrieveUpdateView

#

#
#urlpatterns = [
#    path('register/', RegisterUserView.as_view(), name='register'),
#    path('login/', LoginView.as_view(), name='login'),
    
#    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
#    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
#    path('doctors/<int:pk>/', DoctorRetrieveUpdateView.as_view(), name='doctor-detail'),
#    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
#    path('patients/<int:pk>/', PatientRetrieveUpdateView.as_view(), name='patient-detail'),
#    
#    path('programs/', ProgramListCreateView.as_view(), name='program-list-create'),
#    path('programs/<int:pk>/', ProgramRetrieveUpdateView.as_view(), name='program-detail'),
#    path('insurance-providers/', InsuranceProviderListCreateView.as_view(), name='insuranceprovider-list-create'),
#    path('insurance-providers/<int:pk>/', InsuranceProviderRetrieveUpdateView.as_view(), name='insuranceprovider-detail'),
#    path('claims/', ClaimListCreateView.as_view(), name='claim-list-create'),
#    path('claims/<int:pk>/', ClaimRetrieveUpdateView.as_view(), name='claim-detail'),
#    path('pharmacies/', PharmacyListCreateView.as_view(), name='pharmacy-list-create'),
#    path('pharmacies/<int:pk>/', PharmacyRetrieveUpdateView.as_view(), name='pharmacy-detail'),
#    path('pharmacy-items/', PharmacyItemListCreateView.as_view(), name='pharmacyitem-list-create'),
#    path('pharmacy-items/<int:pk>/', PharmacyItemRetrieveUpdateView.as_view(), name='pharmacyitem-detail'),
#    path('nurses/', NurseListCreateView.as_view(), name='nurse-list-create'),
#    path('nurses/<int:pk>/', NurseRetrieveUpdateView.as_view(), name='nurse-detail'),
#    path('labtechnicians/', LabTechnicianListCreateView.as_view(), name='labtechnician-list-create'),
#    path('labtechnicians/<int:pk>/', LabTechnicianRetrieveUpdateView.as_view(), name='labtechnician-detail'),
#    path('pharmacists/', PharmacistListCreateView.as_view(), name='pharmacist-list-create'),
#    path('pharmacists/<int:pk>/', PharmacistRetrieveUpdateView.as_view(), name='pharmacist-detail'),
#    path('receptionists/', ReceptionistListCreateView.as_view(), name='receptionist-list-create'),
#    path('receptionists/<int:pk>/', ReceptionistRetrieveUpdateView.as_view(), name='receptionist-detail'),
#    path('financestaff/', FinanceStaffListCreateView.as_view(), name='financestaff-list-create'),
#    path('financestaff/<int:pk>/', FinanceStaffRetrieveUpdateView.as_view(), name='financestaff-detail'),
#    path('facilities/', FacilityListCreateView.as_view(), name='facility-list-create'),
#    path('facilities/<int:pk>/', FacilityRetrieveUpdateView.as_view(), name='facility-detail'),
#]
#
