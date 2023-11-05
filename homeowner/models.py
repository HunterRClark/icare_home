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
    mortgage_details = models.TextField(_("Mortgage Details"), blank=True, null=True)
    insurance_details = models.TextField(_("Insurance Details"), blank=True, null=True)
    lawn_size = models.DecimalField(_("Lawn Size"), max_digits=7, decimal_places=2, blank=True, null=True)
    flower_bed_size = models.DecimalField(_("Flower Bed Size"), max_digits=7, decimal_places=2, blank=True, null=True)
    number_of_trees = models.IntegerField(_("Number of Trees"), default=0)
    internet_service_provider = models.CharField(max_length=255, blank=True, null=True)
    internet_plan = models.CharField(max_length=255, blank=True, null=True)
    internet_speed = models.CharField(max_length=255, blank=True, null=True)
    # You might also include a field for the contract or renewal date, if relevant
    internet_contract_renewal_date = models.DateField(blank=True, null=True)
    # ... other fields from external services ...

    def __str__(self):
        return f"{self.address} ({self.owner.username})"
