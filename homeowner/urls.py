# homeowner/urls.py
from django.urls import path
from .views import RegisterView

app_name = 'homeowner'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    # Add other URL patterns for homeowner app here
]
