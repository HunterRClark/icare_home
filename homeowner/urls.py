# homeowner/urls.py
from django.urls import path
from .views import views

app_name = 'homeowner'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('profile/edit/', views.ProfileView.as_view(), name='edit_profile'),
    path('homes/', views.HomeListView.as_view(), name='home_list'),
    path('homes/add/', views.HomeCreateView.as_view(), name='home_add'),
    path('homes/<int:pk>/edit/', views.HomeUpdateView.as_view(), name='home_edit'),
    path('homes/<int:pk>/delete/', views.HomeDeleteView.as_view(), name='home_delete'),
    # Add other URL patterns for homeowner app here
]
