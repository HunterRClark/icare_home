# homeowner/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Home

# Your existing UserRegisterForm
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

        # Create or update the profile instance
        Profile.objects.update_or_create(user=user)
        return user

# Form for user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone_number', 'first_name', 'last_name', 'email']  # Add other fields as required
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            # Add widgets for other fields
        }

    # If the first_name, last_name, and email fields are part of the User model, not Profile, 
    # you need to add these fields manually and handle them in the save method.
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # Initialize form fields with instance data if available
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        profile = super(ProfileForm, self).save(commit=False)
        if commit:
            user = profile.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.save()
            profile.save()
        return profile

# Form for homes
class HomeForm(forms.ModelForm):
    class Meta:
        model = Home
        fields = [
            'address', 'floor_plan', 'number_of_bedrooms', 'number_of_bathrooms', 
            'number_of_living_rooms', 'total_floor_space', 'lawn_size', 'flower_bed_size',
            'number_of_trees', 'internet_service_provider', 'internet_plan', 'internet_speed', 
            'internet_contract_end_date', 'mortgage_lender', 'mortgage_amount', 
            'mortgage_monthly_payment', 'mortgage_interest_rate', 'mortgage_start_date', 
            'mortgage_end_date', 'insurance_provider', 'insurance_policy_number', 
            'insurance_coverage_amount', 'insurance_premium', 'insurance_start_date', 
            'insurance_end_date'
        ]
        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'floor_plan': forms.FileInput(attrs={'class': 'form-control-file'}),
            'number_of_bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_living_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_floor_space': forms.NumberInput(attrs={'class': 'form-control'}),
            'lawn_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'flower_bed_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_trees': forms.NumberInput(attrs={'class': 'form-control'}),
            'internet_service_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'internet_plan': forms.TextInput(attrs={'class': 'form-control'}),
            'internet_speed': forms.TextInput(attrs={'class': 'form-control'}),
            'internet_contract_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mortgage_lender': forms.TextInput(attrs={'class': 'form-control'}),
            'mortgage_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'mortgage_monthly_payment': forms.NumberInput(attrs={'class': 'form-control'}),
            'mortgage_interest_rate': forms.NumberInput(attrs={'class': 'form-control'}),
            'mortgage_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mortgage_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'insurance_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_policy_number': forms.TextInput(attrs={'class': 'form-control'}),
            'insurance_coverage_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'insurance_premium': forms.NumberInput(attrs={'class': 'form-control'}),
            'insurance_start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'insurance_end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }