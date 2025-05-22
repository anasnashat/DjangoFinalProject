from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileShowView.as_view(), name='profile'),
    path('update_profile/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('delete_profile/', views.UserProfileDeleteView.as_view(), name='delete_profile'),
    path('profile/projects/', views.UserProjectsListView.as_view(), name='user_projects'),
    path('profile/donations/', views.UserDonationsListView.as_view(), name='user_donations'),
]