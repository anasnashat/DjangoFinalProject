from django.urls import path
from . import views

urlpatterns = [
    path('create-session/<slug:slug>/', views.create_donation_session, name='create-payment-session'),
    path('success/<slug:slug>', views.payment_success, name='payment-success')
]