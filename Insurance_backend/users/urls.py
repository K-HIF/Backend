# users/urls.py
from django.urls import path
from .views import RegisterUserView, LoginView
from django.http import JsonResponse
from .views import payback_view
def health_check(request):
    return JsonResponse({'status': 'ok'})

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path("health/", health_check),
    path('payback/', payback_view, name='payback'),
]