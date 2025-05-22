from django.shortcuts import render, redirect
from django.views.generic import DetailView, UpdateView, DeleteView, ListView
from django.urls import reverse_lazy
from projects.models import Profile, Project, Donation
from projects.forms import ProfileUpdateForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect

class UserProfileShowView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'projects/profile.html'
    context_object_name = 'profile'
    
    def get_object(self):
        return self.request.user.profile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projects'] = self.request.user.project_set.all()
        context['donations'] = self.request.user.donation_set.all()
        return context

class UserProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'projects/update_profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user.profile
    
    def form_valid(self, form):
        messages.success(self.request, 'Profile updated successfully!')
        return super().form_valid(form)

class UserProfileDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'projects/delete_profile.html'
    success_url = reverse_lazy('home')
    
    def get_object(self):
        return self.request.user
    
    def post(self, request, *args, **kwargs):
        password = request.POST.get('password')
        user = authenticate(username=request.user.username, password=password)
        
        if user is not None:
            messages.success(request, 'Profile deleted successfully!')
            return super().post(request, *args, **kwargs)
        else:
            messages.error(request, 'Incorrect password. Please try again.')
            return HttpResponseRedirect(reverse_lazy('delete_profile'))

class UserProjectsListView(LoginRequiredMixin, ListView):
    model = Project
    template_name = 'projects/user_projects.html'
    context_object_name = 'projects'
    paginate_by = 10
    
    def get_queryset(self):
        return Project.objects.filter(created_by=self.request.user).order_by('-created_at')

class UserDonationsListView(LoginRequiredMixin, ListView):
    model = Donation
    template_name = 'projects/user_donations.html'
    context_object_name = 'donations'
    paginate_by = 10
    
    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user).order_by('-created_at')
