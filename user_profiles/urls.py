from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserProfileShowView.as_view(), name='profile'),
    path('update/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('delete/', views.UserProfileDeleteView.as_view(), name='delete_profile'),
    path('projects/', views.UserProjectsListView.as_view(), name='user_projects'),
    path('donations/', views.UserDonationsListView.as_view(), name='user_donations'),
]
