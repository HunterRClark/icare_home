# homeowner/models.py

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile'
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    number_of_phones = models.PositiveIntegerField(default=0, blank=True, null=True, verbose_name=_("Number of Phones"))
    phone_plan_provider = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Phone Plan Provider"))
    phone_plan_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name=_("Monthly Cost"))
    phone_plan_data_limit = models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Data Limit"))
    phone_plan_contract_end_date = models.DateField(blank=True, null=True, verbose_name=_("Contract End Date"))
    # Additional fields can be added here if needed for the homeowner's personal details

    def __str__(self):
        return f"{self.user.username}'s profile"

class Home(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='homes'
    )
    address = models.CharField(_("Home Address"), max_length=255)
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
    internet_monthly_payment = models.CharField(max_length=255, blank=True, null=True)
    current_internet_speed = models.CharField(max_length=255, blank=True, null=True)
    recommended_internet_speed = models.CharField(max_length=255, blank=True, null=True)
    # You might also include a field for the contract or renewal date, if relevant
    internet_contract_end_date = models.DateField(blank=True, null=True)
    # ... other fields from external services ...

    def __str__(self):
        return f"{self.address} ({self.owner.username})"
