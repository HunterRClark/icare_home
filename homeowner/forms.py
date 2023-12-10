# homeowner/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Home, Business, Invitation, Deal, LandscapingServiceRequest, LandscapingService

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    business_name = forms.CharField(required=False, max_length=255)
    business_address = forms.CharField(required=False, max_length=255)
    user_type = forms.ChoiceField(choices=Profile.USER_TYPE_CHOICES, required=True, label="I am registering as a")
    business_type = forms.ChoiceField(choices=Profile.BUSINESS_TYPES, required=False, label="Business Type")
    zip_code = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={'placeholder': 'Zip Code'})
    )
    landscaping_services_offered = forms.ModelMultipleChoiceField(
        queryset=LandscapingService.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Landscaping Services Offered"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'user_type', 'business_name', 'business_type', 'business_address', 'zip_code', 'landscaping_services_offered']

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        # Hide the landscaping_services_offered field initially
        self.fields['landscaping_services_offered'].widget.attrs['style'] = 'display;'

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            profile_defaults = {
                'user_type': self.cleaned_data['user_type'],
                'phone_number': self.cleaned_data.get('phone_number', ''),
                'business_name': self.cleaned_data.get('business_name', ''),
                'business_type': self.cleaned_data.get('business_type', ''),
                'zip_code': self.cleaned_data.get('zip_code', '') if self.cleaned_data['user_type'] == 'business' else None,
                'business_address': self.cleaned_data.get('business_address', '')
            }
            Profile.objects.update_or_create(user=user, defaults=profile_defaults)

            if self.cleaned_data['user_type'] == 'business':
                business_instance = Business.objects.create(
                    name=self.cleaned_data['business_name'],
                    address=self.cleaned_data['business_address'],
                    zip_code=self.cleaned_data['zip_code'],
                    business_type=self.cleaned_data['business_type'],
                    owner=user
                )

                # Set landscaping services only for landscaping businesses
                if self.cleaned_data['business_type'] == 'Landscaping':
                    business_instance.landscaping_services_offered.set(self.cleaned_data['landscaping_services_offered'])

        return user

# Form for user profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'phone_number', 'first_name', 'last_name', 'email','number_of_phones',
            'phone_plan_provider','phone_plan_cost','phone_plan_data_limit','phone_plan_contract_end_date',
        ]  # Add other fields as required
        widgets = {
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'number_of_phones': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Number of Phones'}),
            'phone_plan_provider': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name of Phone Providor'}),
            'phone_plan_cost': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Phone Plan Cost'}),
            'phone_plan_data_limit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Phone Data Plan'}),
            'phone_plan_contract_end_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Plan Contract End Date'}),
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
            'number_of_trees', 'internet_service_provider', 'internet_monthly_payment', 'current_internet_speed', 
            'internet_contract_end_date', 'mortgage_lender', 'mortgage_amount', 
            'mortgage_monthly_payment', 'mortgage_interest_rate', 'mortgage_start_date', 
            'mortgage_end_date', 'insurance_provider', 'insurance_policy_number', 
            'insurance_coverage_amount', 'insurance_premium', 'insurance_start_date', 
            'insurance_end_date','recommended_internet_speed', 'zip_code'
        ]

        widgets = {
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zip_code': forms.NumberInput(attrs={'class': 'form-control'}),
            'floor_plan': forms.FileInput(attrs={'class': 'form-control-file'}),
            'number_of_bedrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_bathrooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_living_rooms': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_floor_space': forms.NumberInput(attrs={'class': 'form-control'}),
            'lawn_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'flower_bed_size': forms.NumberInput(attrs={'class': 'form-control'}),
            'number_of_trees': forms.NumberInput(attrs={'class': 'form-control'}),
            'internet_service_provider': forms.TextInput(attrs={'class': 'form-control'}),
            'internet_monthly_payment': forms.TextInput(attrs={'class': 'form-control'}),
            'current_internet_speed': forms.TextInput(attrs={'class': 'form-control'}),
            'reccomended_internet_speed': forms.TextInput(attrs={'class': 'form-control'}),
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

class InternetDealsForm(forms.ModelForm):
    home_address = forms.ModelChoiceField(
        queryset=Home.objects.none(),
        empty_label="Select a Home",
        to_field_name="address",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Home
        fields = ['home_address', 'current_internet_speed', 'recommended_internet_speed', 'internet_monthly_payment', 'internet_price_threshold']
        labels = {
            'current_internet_speed': 'Current Internet Speed (Mbps)',
            'recommended_internet_speed': 'Recommended Internet Speed (Mbps)',
            'internet_monthly_payment': 'Monthly Payment ($)',
            'internet_price_threshold': 'Max Price For Better Internet'
        }
        widgets = {
            'current_internet_speed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current Internet Speed (Mbps)'}),
            'recommended_internet_speed': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Recommended Internet Speed (Mbps)'}),
            'internet_monthly_payment': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Monthly Payment ($)'}),
            'internet_price_threshold': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Max Accepted Price For Better Internet'}),
        }
        help_texts = {
            'recommended_internet_speed': ('Not sure what speed you need? '
                                           '<a href="https://www.highspeedinternet.com/how-much-internet-speed-do-i-need" target="_blank">Find out here</a>.')
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(InternetDealsForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['home_address'].queryset = Home.objects.filter(owner=user)

class InvitationForm(forms.ModelForm):
    class Meta:
        model = Invitation
        fields = ['email']

    def __init__(self, *args, **kwargs):
        self.business = kwargs.pop('business', None)
        super(InvitationForm, self).__init__(*args, **kwargs)
        self.fields['email'].label = "Invitee's Email Address"

class DealForm(forms.ModelForm):
    class Meta:
        model = Deal
        fields = ['zip_code', 'provider_name', 'internet_speed_offered', 'monthly_cost', 'deal_expiration_date']

    def __init__(self, *args, **kwargs):
        business = kwargs.pop('business', None)
        super(DealForm, self).__init__(*args, **kwargs)

        if business and business.business_type == 'Internet':
            self.fields['zip_code'].initial = business.zip_code
            self.fields['zip_code'].widget = forms.HiddenInput()
            # Retain only relevant fields for Internet providers
            self.fields['provider_name'].initial = business.name
            del self.fields['deal_expiration_date']  # Remove if not relevant
            # Add other adjustments as needed

class LandscapingDealsForm(forms.ModelForm):
    SERVICE_TYPE_CHOICES = [
        ('', 'Choose a service...'),
        ('lawn_mowing', 'Lawn Mowing'),
        ('tree_trimming', 'Tree Trimming'),
        ('lawn_care', 'Lawn Care'),
    ]
    service_type = forms.ChoiceField(
        choices=SERVICE_TYPE_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={
            'class': 'form-control', 
            'onchange': 'updateLandscapingFields()'
        })
    )
    # Assuming these fields are already part of the Home model
    lawn_size = forms.DecimalField(
        max_digits=7, 
        decimal_places=2, 
        required=False, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Area of Lawn (sqft)'
        }),
        help_text='Not sure of your lawn size? <a href="https://www.measuremylawn.com/" target="_blank">Measure it here</a>.'
    )
    flower_bed_size = forms.DecimalField(
        max_digits=7, 
        decimal_places=2, 
        required=False, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Area of Flower Beds (sqft)'
        })
    )
    number_of_trees = forms.IntegerField(
        required=False, 
        widget=forms.NumberInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Total Number of Trees'
        })
    )

    class Meta:
        model = Home
        fields = ['lawn_size', 'flower_bed_size', 'number_of_trees']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(LandscapingDealsForm, self).__init__(*args, **kwargs)
        # Initialize these fields with existing data from the user's home
        if user:
            home = Home.objects.filter(owner=user).first()
            if home:
                self.fields['lawn_size'].initial = home.lawn_size
                self.fields['flower_bed_size'].initial = home.flower_bed_size
                self.fields['number_of_trees'].initial = home.number_of_trees