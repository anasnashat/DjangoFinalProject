from django.urls import path
from . import views

app_name = 'donations'

urlpatterns = [
    path('create-session/<slug:slug>/', views.create_donation_session, name='donation-create'),
    path('success/<slug:slug>/', views.payment_success, name='donation-success'),
]