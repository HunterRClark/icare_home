# homeowner/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import UserRegisterForm, ProfileForm, HomeForm, InvitationForm, InternetDealsForm, DealForm, LandscapingDealsForm
from .models import Profile, Home, Notification, Invitation, Business, Deal, match_internet_deals, LandscapingServiceRequest, LandscapingService
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect, HttpResponseForbidden
import logging

# Set up logging (typically at the top of the file)
logger = logging.getLogger(__name__)

def notify_landscaping_businesses(home, service_type):
    landscaping_businesses = Business.objects.filter(
        business_type='Landscaping',
        landscaping_services_offered__service_type=service_type
    )
    for business in landscaping_businesses:
        Notification.objects.create(
            user=business.owner,
            title="New Landscaping Opportunity",
            message=f"A new request for {service_type} is available in your area for {home.address}.",
            notification_type='deal'
        )

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
        queryset = self.request.user.homes.all()
        print(queryset)  # This will print to your console
        return queryset

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

    def form_valid(self, form):
        # The form is already valid here, so you can save it directly
        self.object = form.save()
        messages.success(self.request, "Home updated successfully!")
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        # Log the form errors
        logger.error("Form is not valid: %s", form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(self.request, f"Error in the {field}: {error}")
        
        # If the form is invalid, this method will be called
        messages.error(self.request, "Error updating home. Please check the form for errors.")
        return self.render_to_response(self.get_context_data(form=form))

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
# Dashboard class        
@method_decorator(login_required, name='dispatch')
class DashboardView(generic.TemplateView):
    template_name = 'homeowner/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Ensure the user has a profile, create one if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=user)
        context['profile'] = profile

        # Fetch homes and handle the case where there are none
        homes = Home.objects.filter(owner=user)
        if homes.exists():
            context['homes'] = homes

            # Retrieve the selected home ID from the session
            selected_home_id = self.request.session.get('selected_home_id', None)
            if selected_home_id is None:
                selected_home_id = homes.first().id
                self.request.session['selected_home_id'] = selected_home_id

            selected_home = Home.objects.get(id=selected_home_id)
            context['selected_home_id'] = selected_home_id
            context['internet_deals_form'] = InternetDealsForm(instance=selected_home)

            # Initialize the LandscapingDealsForm with initial values
            initial_landscaping_data = {
                'lawn_size': selected_home.lawn_size,
                'flower_bed_size': selected_home.flower_bed_size,
                'number_of_trees': selected_home.number_of_trees
            }
            context['landscaping_deals_form'] = LandscapingDealsForm(initial=initial_landscaping_data)
        else:
            context['no_homes_message'] = "No homes added yet."
            context['internet_deals_form'] = InternetDealsForm()  # Initialize an empty form
            initial_landscaping_data = {}  # Initialize with empty data
            context['landscaping_deals_form'] = LandscapingDealsForm(initial=initial_landscaping_data)

        # Fetch unread notifications
        context['notifications'] = Notification.objects.filter(user=user, read=False)

        return context

    def post(self, request, *args, **kwargs):
        print("Form submitted")
        selected_home_id = request.POST.get('selected_home_id')
        print("In post method, selected_home_id from POST:", selected_home_id)

        if selected_home_id:
            selected_home = Home.objects.get(id=selected_home_id)
            request.session['selected_home_id'] = selected_home_id
            request.session.save()

            if 'submit_deals_form' in request.POST:
                print("Deals form submitted")
                print("POST data:", request.POST)
            
                # Manually update the selected home with form data
                selected_home.current_internet_speed = request.POST.get('current_internet_speed')
                selected_home.recommended_internet_speed = request.POST.get('recommended_internet_speed')
                selected_home.internet_monthly_payment = request.POST.get('internet_monthly_payment')
                selected_home.save()

                print("Updated Home:", selected_home)
                messages.success(request, 'Your internet deal information has been updated.')
                return redirect('homeowner:dashboard')

            elif 'submit_landscaping_form' in request.POST:
                print("Landscaping form submitted")
                print("POST data:", request.POST)

                landscaping_form = LandscapingDealsForm(request.POST)
                if landscaping_form.is_valid():
                    # Create a new LandscapingServiceRequest instance
                    LandscapingServiceRequest.objects.create(
                        home=selected_home,
                        service_type=landscaping_form.cleaned_data['service_type']
                    )

                    # Notify landscaping businesses
                    notify_landscaping_businesses(selected_home, landscaping_form.cleaned_data['service_type'])

                    messages.success(request, 'Your landscaping service request has been submitted.')
                else:
                    messages.error(request, 'There was an error with your landscaping service request submission.')

                return redirect('homeowner:dashboard')
            else:
                print("Not a deals form submission")

        context = self.get_context_data(**kwargs)
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class MarkNotificationReadView(View):
    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get('notification_id')
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.read = True
        notification.save()
        # Redirect to the appropriate dashboard based on user type
        if request.user.profile.user_type == 'business':
            return redirect('homeowner:business_dashboard')
        else:
            return redirect('homeowner:dashboard')

@method_decorator(login_required, name='dispatch')
class DealListView(generic.ListView):
    model = Home  # Assuming the deal preferences are stored in the Home model
    template_name = 'homeowner/deal_list.html'
    context_object_name = 'deals'

    def get_queryset(self):
        return self.request.user.homes.all()


@method_decorator(login_required, name='dispatch')
class BusinessDashboardView(generic.TemplateView):
    template_name = 'homeowner/business_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        business = Business.objects.filter(owner=self.request.user).first()

        # Redirect if the user is not associated with any business
        if not business:
            return redirect('homeowner:dashboard')

        profile = self.request.user.profile

        # Redirect if not a business user
        if profile.user_type != 'business':
            return redirect('homeowner:dashboard')

        # Fetch unread notifications for the business user
        context['notifications'] = Notification.objects.filter(
            user=self.request.user, 
            read=False
        )

        # Business-specific context
        context['profile'] = profile
        context['business'] = business  # Added business object to context
        context['business_type'] = business.business_type  # Added business type to context
        context['invitation_form'] = InvitationForm()
        context['create_deal_form'] = DealForm(business=business)
        return context

@method_decorator(login_required, name='dispatch')
class DashboardRedirectView(View):
    def get(self, request, *args, **kwargs):
        if request.user.profile.user_type == 'business':
            return redirect('homeowner:business_dashboard')
        else:
            return redirect('homeowner:dashboard')

@method_decorator(login_required, name='dispatch')
class SendInvitationView(generic.CreateView):
    model = Invitation
    form_class = InvitationForm
    template_name = 'homeowner/send_invitation.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.profile.is_business_admin:
            return HttpResponseForbidden("You do not have permission to access this page.")
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        kwargs = super(SendInvitationView, self).get_form_kwargs()
        # Assuming the Business model is linked to the User model
        user_business = Business.objects.filter(owner=self.request.user).first()
        kwargs.update({'business': user_business})  # Pass the business instance to the form
        return kwargs

    def form_valid(self, form):
        invitation = form.save(commit=False)
        invitation.sender = self.request.user  # Set the sender to the current logged-in user
        invitation.save()

        # Here, you can add the logic to send an email invitation
        messages.success(self.request, "Invitation sent successfully!")
        return redirect('homeowner:dashboard')

@method_decorator(login_required, name='dispatch')
class CreateDealView(generic.CreateView):
    model = Deal
    form_class = DealForm
    template_name = 'homeowner/create_deal.html'

    def get_form_kwargs(self):
        kwargs = super(CreateDealView, self).get_form_kwargs()
        business = self.request.user.business  # Assuming each User has a related Business instance
        kwargs.update({'business': business})
        return kwargs

    def form_valid(self, form):
        deal = form.save(commit=False)
        deal.business = self.request.user  # Assign the User instance directly
        deal.deal_type = self.request.user.business.business_type.lower()  # Set deal type based on the business type
        deal.save()

        # Call the matching logic after saving the deal
        match_internet_deals(deal)

        return super(CreateDealView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('homeowner:business_dashboard')
    
