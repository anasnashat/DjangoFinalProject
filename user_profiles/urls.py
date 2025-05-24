from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.UserProfileShowView.as_view(), name='profile'),
    path('update_profile/', views.UserProfileUpdateView.as_view(), name='update_profile'),
    path('delete_profile/', views.UserProfileDeleteView.as_view(), name='delete_profile'),
]