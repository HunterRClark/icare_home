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
    DashboardRedirectView,
    DashboardView,
    SendInvitationView,
    CreateDealView,
    BusinessOpportunityReportView
)

app_name = 'homeowner'

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='edit_profile'),
    path('homes/', HomeListView.as_view(), name='home_list'),
    path('homes/add/', HomeCreateView.as_view(), name='home_add'),
    path('homes/<int:pk>/', HomeDetailView.as_view(), name='home_detail'),
    path('homes/<int:pk>/edit/', HomeUpdateView.as_view(), name='home_edit'),
    path('homes/<int:pk>/delete/', HomeDeleteView.as_view(), name='home_delete'),
    path('dashboard-redirect/', DashboardRedirectView.as_view(), name='dashboard_redirect'),  # Updated path for dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('notifications/mark-as-read/', MarkNotificationReadView.as_view(), name='mark_notification_read'),
    path('deals/', DealListView.as_view(), name='deal_list'),
    path('business-dashboard/', BusinessDashboardView.as_view(), name='business_dashboard'),
    path('send-invitation/', SendInvitationView.as_view(), name='send_invitation'),
    path('create-deal/', CreateDealView.as_view(), name='create_deal'),
    path('business-opportunity-report/', BusinessOpportunityReportView.as_view(), name='business_opportunity_report'),
    # Add other URL patterns for homeowner app here
]

