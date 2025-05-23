from django.shortcuts import render
from django.views.generic import DetailView, UpdateView, DeleteView
from django.urls import reverse_lazy
from projects.models import Profile
from projects.forms import ProjectForm
from django.contrib.auth.mixins import LoginRequiredMixin

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

class UserProfileUpdateView(UpdateView):
	pass

class UserProfileDeleteView(DeleteView):
	pass
