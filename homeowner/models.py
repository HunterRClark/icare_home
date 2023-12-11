# homeowner/models.py

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
import uuid
import datetime

class Profile(models.Model):
    USER_TYPE_CHOICES = [
        ('homeowner', 'Homeowner'),
        ('business', 'Business'),
    ]

    BUSINESS_TYPES = [
        ('Internet', 'Internet Service Provider'),
        ('Landscaping', 'Landscaping Services'),
        ('PhonePlans', 'Phone Plan Services'),
        # Add more business types as needed
    ]

    business_type = models.CharField(max_length=50, choices=BUSINESS_TYPES, blank=True, null=True, verbose_name=_("Business Type"))

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='homeowner')
    is_business_admin = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    # Business-specific fields
    business_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Business Name"))
    business_address = models.CharField(max_length=255, default='BadAddress', verbose_name=_("Business Address"))
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999),MinValueValidator(10000)], default=11111, verbose_name=_("Zip Code"))


    # Fields specific to homeowners
    number_of_phones = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_("Number of Phones"), help_text="Applicable for homeowners")
    phone_plan_provider = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Phone Plan Provider"), help_text="Applicable for homeowners")
    phone_plan_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Monthly Cost"), help_text="Applicable for homeowners")
    phone_plan_data_limit = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Data Limit"), help_text="Applicable for homeowners")
    phone_plan_contract_end_date = models.DateField(blank=True, null=True, verbose_name=_("Contract End Date"), help_text="Applicable for homeowners")
    
    # Add additional fields for business users here if needed

    def __str__(self):
        return f"{self.user.username}'s profile - {self.get_user_type_display()}"

class Home(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='homes'
    )
    internet_price_threshold = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    address = models.CharField(_("Home Address"), max_length=255)
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999),MinValueValidator(10000)], default=11111, verbose_name=_("Zip Code"))
    # Mortgage Details
    mortgage_lender = models.CharField(max_length=255, blank=True, null=True)
    mortgage_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mortgage_monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mortgage_interest_rate = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    mortgage_start_date = models.DateField(blank=True, null=True)
    mortgage_end_date = models.DateField(blank=True, null=True)
    # Insurance Details
    insurance_provider = models.CharField(max_length=255, blank=True, null=True)
    insurance_policy_number = models.CharField(max_length=255, blank=True, null=True)
    insurance_coverage_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    insurance_premium = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    insurance_start_date = models.DateField(blank=True, null=True)
    insurance_end_date = models.DateField(blank=True, null=True)
    # Interior Details
    floor_plan = models.ImageField(upload_to='floor_plans/', blank=True, null=True)
    number_of_bedrooms = models.PositiveIntegerField(_("Number of Bedrooms"), default=0, blank=True, null=True)
    number_of_bathrooms = models.PositiveIntegerField(_("Number of Bathrooms"), default=0, blank=True, null=True)
    number_of_living_rooms = models.PositiveIntegerField(_("Number of Living Rooms"), default=0, blank=True, null=True)
    total_floor_space = models.DecimalField(_("Total Floor Space (sqft)"), max_digits=10, decimal_places=2, blank=True, null=True)
    #Exterior Details
    lawn_size = models.DecimalField(_("Area of Lawn (sqft)"), max_digits=7, decimal_places=2, blank=True, null=True)
    flower_bed_size = models.DecimalField(_("Flower Bed Size"), max_digits=7, decimal_places=2, blank=True, null=True)
    number_of_trees = models.IntegerField(_("Number of Trees"), default=0)
    #internet details
    internet_service_provider = models.CharField(max_length=255, blank=True, null=True)
    internet_monthly_payment = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    current_internet_speed = models.PositiveIntegerField(blank=True, null=True)
    recommended_internet_speed = models.PositiveIntegerField(blank=True, null=True)
    # You might also include a field for the contract or renewal date, if relevant
    internet_contract_end_date = models.DateField(blank=True, null=True)
    # ... other fields from external services ...

    def __str__(self):
        return f"{self.address} ({self.owner.username})"

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('deal', 'Deal'),
        ('system', 'System'),
        # Add more types as needed
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='notifications'
    )
    deal = models.ForeignKey(
        'Deal',  # Replace with the actual name of your Deal model if it's different
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='notifications'
    )
    title = models.CharField(max_length=255)
    message = models.TextField()
    notification_type = models.CharField(max_length=10, choices=NOTIFICATION_TYPES, default='system')
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.user.username}"

class EmailInvitation(models.Model):
    email = models.EmailField()
    token = models.CharField(max_length=64, unique=True)
    business = models.ForeignKey('Profile', on_delete=models.CASCADE, limit_choices_to={'user_type': 'business'})
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.token:
            self.token = get_random_string(64)
        if not self.expires_at:
            self.expires_at = timezone.now() + datetime.timedelta(days=7)  # Set expiration for 7 days from now
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invitation to {self.email} from {self.business.business_name}"

class Invitation(models.Model):
    email = models.EmailField()
    business = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='invitations')
    token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Invitation to {self.email} from {self.business}"

class Deal(models.Model):
    DEAL_TYPES = [
        ('internet', 'Internet'),
        ('landscaping', 'Landscaping'),
        # Add more deal types as needed
    ]

    zip_code = models.CharField(max_length=5)
    deal_type = models.CharField(max_length=15, choices=DEAL_TYPES)
    provider_name = models.CharField(max_length=255)
    internet_speed_offered = models.PositiveIntegerField()  # In Mbps
    monthly_cost = models.DecimalField(max_digits=10, decimal_places=2)
    deal_expiration_date = models.DateField(blank=True, null=True)
    business = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deals')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.provider_name} - {self.deal_type} deal"

class LandscapingServiceRequest(models.Model):
    SERVICE_CHOICES = [
        ('lawn_mowing', 'Lawn Mowing'),
        ('tree_trimming', 'Tree Trimming'),
        ('lawn_care', 'Lawn Care')
    ]
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name='landscaping_requests')
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    request_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_service_type_display()} request for {self.home.address} on {self.request_date}"

class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999),MinValueValidator(10000)], default=11111, verbose_name=_("Zip Code"))
    business_type = models.CharField(max_length=255)
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='business')

    # Changed to ManyToManyField to represent multiple landscaping services
    landscaping_services_offered = models.ManyToManyField(
        'LandscapingService',
        blank=True
    )

    def __str__(self):
        return self.name

class LandscapingService(models.Model):
    SERVICE_CHOICES = [
        ('lawn_mowing', 'Lawn Mowing'),
        ('tree_trimming', 'Tree Trimming'),
        ('lawn_care', 'Lawn Care'),
    ]
    service_type = models.CharField(max_length=50, choices=SERVICE_CHOICES, unique=True)

    def __str__(self):
        return self.get_service_type_display()

def match_internet_deals(deal):
    print(f"Matching deals for: {deal}")
    if deal.deal_type != 'internet':
        return  # Only process internet deals

    for home in Home.objects.filter(zip_code=deal.zip_code):
        print(f"Checking deal for home: {home.address}")
        # Check if deal offers better conditions
        is_speed_better = deal.internet_speed_offered > home.current_internet_speed
        is_price_better = deal.monthly_cost < home.internet_monthly_payment
        meets_recommended_speed = deal.internet_speed_offered >= home.recommended_internet_speed
        within_price_threshold = deal.monthly_cost <= home.internet_price_threshold

        if (is_speed_better and not is_price_better) and not within_price_threshold:
            continue  # Skip if speed is better but price is higher than the user's threshold

        if is_speed_better or is_price_better or (meets_recommended_speed and within_price_threshold):
            print(f"Creating notification for user: {home.owner}")
            create_notification(home.owner, deal)

def create_notification(user, deal):
    title = "New Internet Deal Available!"
    message = f"A new deal from {deal.provider_name} is available: {deal.internet_speed_offered} Mbps for ${deal.monthly_cost} per month."
    Notification.objects.create(user=user, title=title, message=message)

class BusinessOpportunityReport(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name='opportunity_reports')
    created_at = models.DateTimeField(auto_now_add=True)
    report_data = models.TextField()  # Simple text field for MVP

    def __str__(self):
        return f"Opportunity Report for {self.business.name} - {self.created_at.strftime('%Y-%m-%d')}"
