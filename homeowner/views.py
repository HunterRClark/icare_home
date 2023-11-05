# homeowner/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm

class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')  # Redirect to login page after registration
    template_name = 'homeowner/register.html'

