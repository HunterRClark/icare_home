# homeowner/views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import UserRegisterForm, ProfileForm, HomeForm
from .models import Profile, Home
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Existing RegisterView class
class RegisterView(generic.CreateView):
    form_class = UserRegisterForm
    success_url = reverse_lazy('login')
    template_name = 'homeowner/register.html'

# New ProfileView class to view and edit user profile
@method_decorator(login_required, name='dispatch')
class ProfileView(generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'homeowner/profile.html'
    success_url = reverse_lazy('dashboard')  # Replace 'dashboard' with the actual name once implemented

    def get_object(self):
        return Profile.objects.get_or_create(user=self.request.user)[0]

# New HomeListView class to list homes
@method_decorator(login_required, name='dispatch')
class HomeListView(generic.ListView):
    model = Home
    template_name = 'homeowner/home_list.html'

    def get_queryset(self):
        return Home.objects.filter(owner=self.request.user)

# New HomeCreateView class to add a new home
@method_decorator(login_required, name='dispatch')
class HomeCreateView(generic.CreateView):
    model = Home
    form_class = HomeForm
    template_name = 'homeowner/home_form.html'
    success_url = reverse_lazy('dashboard')  # Replace 'dashboard' with the actual name once implemented

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# New HomeUpdateView class to edit an existing home
@method_decorator(login_required, name='dispatch')
class HomeUpdateView(generic.UpdateView):
    model = Home
    form_class = HomeForm
    template_name = 'homeowner/home_form.html'
    success_url = reverse_lazy('dashboard')  # Replace 'dashboard' with the actual name once implemented

# New HomeDeleteView class to delete an existing home
@method_decorator(login_required, name='dispatch')
class HomeDeleteView(generic.DeleteView):
    model = Home
    template_name = 'homeowner/home_confirm_delete.html'
    success_url = reverse_lazy('dashboard')  # Replace 'dashboard' with the actual name once implemented


