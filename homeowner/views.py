# homeowner/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic, View
from .forms import UserRegisterForm, ProfileForm, HomeForm, InternetDealsForm
from .models import Profile, Home, Notification
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
import logging

# Set up logging (typically at the top of the file)
logger = logging.getLogger(__name__)

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
        context['profile'] = Profile.objects.get(user=user)
        context['homes'] = Home.objects.filter(owner=user)
        context['notifications'] = Notification.objects.filter(user=user, read=False)

        # Retrieve the selected home ID from the session
        selected_home_id = self.request.session.get('selected_home_id', None)
        if selected_home_id is None and user.homes.exists():
            selected_home_id = user.homes.first().id
            self.request.session['selected_home_id'] = selected_home_id

        selected_home = Home.objects.get(id=selected_home_id) if selected_home_id else None
        context['selected_home_id'] = selected_home_id
        context['internet_deals_form'] = InternetDealsForm(instance=selected_home)
        print("In get_context_data, selected_home_id:", selected_home_id)
        
        return context

    def post(self, request, *args, **kwargs):
        selected_home_id = request.POST.get('selected_home_id')
        print("In post method, selected_home_id from POST:", selected_home_id) 

        if selected_home_id:
            request.session['selected_home_id'] = selected_home_id
            request.session.save()

        # Refresh context with updated selected_home_id
        context = self.get_context_data(**kwargs)
        context['selected_home_id'] = selected_home_id

        if 'submit_deals_form' in request.POST:
            selected_home = Home.objects.get(id=selected_home_id) if selected_home_id else None
            form = InternetDealsForm(request.POST, instance=selected_home)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your deal information has been updated.')
                return redirect('homeowner:dashboard')
            else:
                context['internet_deals_form'] = form
        print("In post method, selected_home_id to be rendered:", selected_home_id)
        return render(request, self.template_name, context)

@method_decorator(login_required, name='dispatch')
class MarkNotificationReadView(View):
    def post(self, request, *args, **kwargs):
        notification_id = request.POST.get('notification_id')
        notification = get_object_or_404(Notification, id=notification_id, user=request.user)
        notification.read = True
        notification.save()
        return redirect('homeowner:dashboard')

@method_decorator(login_required, name='dispatch')
class DealListView(generic.ListView):
    model = Home  # Assuming the deal preferences are stored in the Home model
    template_name = 'homeowner/deal_list.html'
    context_object_name = 'deals'

    def get_queryset(self):
        return self.request.user.homes.all()