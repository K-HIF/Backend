# users/urls.py
from django.urls import path
from .views import RegisterUserView, LoginView
from django.http import JsonResponse
from .views import payback_view,GoogleLoginView
from .views import DoctorListCreateView, DoctorRetrieveUpdateView
from .views import PatientListCreateView, PatientRetrieveUpdateView
from .views import DepartmentListCreateView, DepartmentRetrieveUpdateView
from .views import ProgramListCreateView, ProgramRetrieveUpdateView
from .views import InsuranceProviderListCreateView, InsuranceProviderRetrieveUpdateView
from .views import ClaimListCreateView, ClaimRetrieveUpdateView
from .views import PharmacyListCreateView, PharmacyRetrieveUpdateView
from .views import PharmacyItemListCreateView, PharmacyItemRetrieveUpdateView
from .views import NurseListCreateView, NurseRetrieveUpdateView
from . import views

def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("health/", health_check),
    path('stars/', payback_view, name='payback'),
    path('downvotes/', views.get_downvotes),
    path('downvote/', views.post_downvote),
    path('google-login/', GoogleLoginView.as_view(), name='google-login'),
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateView.as_view(), name='doctor-detail'),
    path('patients/', PatientListCreateView.as_view(), name='patient-list-create'),
    path('patients/<int:pk>/', PatientRetrieveUpdateView.as_view(), name='patient-detail'),
    path('departments/', DepartmentListCreateView.as_view(), name='department-list-create'),
    path('departments/<int:pk>/', DepartmentRetrieveUpdateView.as_view(), name='department-detail'),
    path('programs/', ProgramListCreateView.as_view(), name='program-list-create'),
    path('programs/<int:pk>/', ProgramRetrieveUpdateView.as_view(), name='program-detail'),
    path('insurance-providers/', InsuranceProviderListCreateView.as_view(), name='insuranceprovider-list-create'),
    path('insurance-providers/<int:pk>/', InsuranceProviderRetrieveUpdateView.as_view(), name='insuranceprovider-detail'),
    path('claims/', ClaimListCreateView.as_view(), name='claim-list-create'),
    path('claims/<int:pk>/', ClaimRetrieveUpdateView.as_view(), name='claim-detail'),
    path('pharmacies/', PharmacyListCreateView.as_view(), name='pharmacy-list-create'),
    path('pharmacies/<int:pk>/', PharmacyRetrieveUpdateView.as_view(), name='pharmacy-detail'),
    path('pharmacy-items/', PharmacyItemListCreateView.as_view(), name='pharmacyitem-list-create'),
    path('pharmacy-items/<int:pk>/', PharmacyItemRetrieveUpdateView.as_view(), name='pharmacyitem-detail'),
    path('nurses/', NurseListCreateView.as_view(), name='nurse-list-create'),
    path('nurses/<int:pk>/', NurseRetrieveUpdateView.as_view(), name='nurse-detail'),
]

