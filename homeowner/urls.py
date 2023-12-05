# homeowner/urls.py
from django.urls import path
from .views import (
    RegisterView,
    ProfileDetailView,
    ProfileUpdateView,
    HomeListView,
    HomeCreateView,
    HomeUpdateView,
    HomeDeleteView,
    HomeDetailView,
    DashboardView,
    MarkNotificationReadView,
    DealListView,
    BusinessDashboardView,
    DashboardRedirectView
)

app_name = 'homeowner'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),  # For viewing the profile
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),  # For editing the profile
    path('homes/', HomeListView.as_view(), name='home_list'),  # List of homes
    path('homes/add/', HomeCreateView.as_view(), name='home_add'),  # Add a new home
    path('homes/<int:pk>/', HomeDetailView.as_view(), name='home_detail'),  # Details of a specific home
    path('homes/<int:pk>/edit/', HomeUpdateView.as_view(), name='home_edit'),  # Edit an existing home
    path('homes/<int:pk>/delete/', HomeDeleteView.as_view(), name='home_delete'),  # Delete an existing home
    path('dashboard/', DashboardView.as_view(), name='dashboard'), # Dashboard View
    path('notifications/mark-as-read/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('deals/', DealListView.as_view(), name='deal_list'),
    path('business-dashboard/', BusinessDashboardView.as_view(), name='business_dashboard'),
    path('dashboard-redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),
    # Add other URL patterns for homeowner app here
]

