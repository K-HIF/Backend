# users/urls.py
from django.urls import path
from .views import RegisterUserView, LoginView
from django.http import JsonResponse
from .views import payback_view,GoogleLoginView
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
]

