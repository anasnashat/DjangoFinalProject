from django.urls import path
from . import views

urlpatterns = [
    path('create-session/<slug:slug>/', views.create_payment_session, name='create-payment-session')
    path('success/', views.payment_success, name='payment-success')
]