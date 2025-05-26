from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from projects.models import Project
from donations.models import Donation
from user_profiles.models import Profile
from user_profiles.forms import ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, logout
from payments.models import Payment

class UserProfileShowView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_projects = self.request.user.project_set.all()
        context['projects'] = user_projects
        context['payments'] = self.request.user.payment_set.all()
        total_raised = sum([project.amount_raised for project in user_projects])
        context['total_amount_raised'] = total_raised
        print(f"Total amount raised by user {self.request.user.username}: {total_raised}")
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profiles/update_profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'profiles/delete_profile.html'
    success_url = reverse_lazy('homepage')
    
    def get_object(self):
        return self.request.user
    
    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            # Store the user object before logging out
            user_to_delete = self.get_object()
            
            # Log out the user first
            logout(request)
            
            # Delete the user object manually
            user_to_delete.delete()
            
            messages.success(request, 'Account deleted successfully!')
            
            # Redirect to success URL
            return HttpResponseRedirect(self.success_url)
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return HttpResponseRedirect(reverse_lazy('delete_profile'))

class UserProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'profiles/user_projects.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user).order_by('-created_at')

class UserDonationsListView(LoginRequiredMixin, ListView):
    template_name = 'profiles/user_donations.html'
    context_object_name = 'donations'
    paginate_by = 10
    
    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by('-created_at')
