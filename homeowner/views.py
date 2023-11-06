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

# ProfileDetailView class to view user profile
@method_decorator(login_required, name='dispatch')
class ProfileDetailView(generic.DetailView):
    model = Profile
    template_name = 'homeowner/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        # Ensure we return the Profile instance for the logged in user
        return self.request.user.profile

# ProfileUpdateView class to edit user profile
@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(generic.UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'homeowner/profile_edit.html'
    success_url = reverse_lazy('homeowner:profile_detail')

    def get_object(self):
        return self.request.user.profile

    def form_valid(self, form):
        user = form.instance.user
        user.email = form.cleaned_data.get('email', user.email)
        user.first_name = form.cleaned_data.get('first_name', user.first_name)
        user.last_name = form.cleaned_data.get('last_name', user.last_name)
        user.save()
        return super().form_valid(form)

# HomeListView class to list homes
@method_decorator(login_required, name='dispatch')
class HomeListView(generic.ListView):
    model = Home
    template_name = 'homeowner/home_list.html'
    context_object_name = 'homes'

    def get_queryset(self):
        return self.request.user.homes.all()

# HomeCreateView class to add a new home
@method_decorator(login_required, name='dispatch')
class HomeCreateView(generic.CreateView):
    model = Home
    form_class = HomeForm
    template_name = 'homeowner/home_form.html'
    success_url = reverse_lazy('homeowner:home_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

# HomeUpdateView class to edit an existing home
@method_decorator(login_required, name='dispatch')
class HomeUpdateView(generic.UpdateView):
    model = Home
    form_class = HomeForm
    template_name = 'homeowner/home_form.html'
    success_url = reverse_lazy('homeowner:home_list')

# HomeDeleteView class to delete an existing home
@method_decorator(login_required, name='dispatch')
class HomeDeleteView(generic.DeleteView):
    model = Home
    template_name = 'homeowner/home_confirm_delete.html'
    success_url = reverse_lazy('homeowner:home_list')

# HomeDetailView class to view details of a home
@method_decorator(login_required, name='dispatch')
class HomeDetailView(generic.DetailView):
    model = Home
    template_name = 'homeowner/home_detail.html'
    context_object_name = 'home'

    def get_queryset(self):
        # This method ensures that a user can only access their own home's details.
        return self.request.user.homes.all()
