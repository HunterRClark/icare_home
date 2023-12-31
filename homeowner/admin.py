from django.contrib import admin
# Register your models here.
from django.contrib import admin
from .models import Profile, Home, Notification, Business, EmailInvitation, Deal, LandscapingService

admin.site.register(Profile)
admin.site.register(Home)
admin.site.register(EmailInvitation)
admin.site.register(Business)
admin.site.register(Deal)
admin.site.register(LandscapingService)

# Optional: Custom Admin for Notification
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created_at', 'read')  # Fields to display in list view
    list_filter = ('read', 'created_at')  # Filters
    search_fields = ('title', 'user__username')  # Enable search by title and username

# Registering Notification with the custom admin (if created)
admin.site.register(Notification, NotificationAdmin)