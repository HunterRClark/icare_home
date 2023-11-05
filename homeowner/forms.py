# homeowner/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Home

# Your existing UserRegisterForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number',]  # Add any other fields you have in your Profile model
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'Enter phone number'}),
            # Include widgets for other fields if necessary
        }

# Form for homes
class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = ['address', 'lawn_size', 'number_of_trees', 'internet_service_provider', 'internet_plan', 'internet_speed', 'contract_end_date']  # Include all the Home model fields here
