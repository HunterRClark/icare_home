# core/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    user = request.user
    if hasattr(user, 'profile'):
        if user.profile.user_type == 'business':
            return redirect('homeowner:business_dashboard')  # Replace with your business dashboard URL name
        else:
            return redirect('homeowner:dashboard')  # Replace with your homeowner dashboard URL name
    return render(request, 'core/home.html')

