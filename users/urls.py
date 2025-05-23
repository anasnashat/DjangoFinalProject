from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    #Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),


    # Email confirmation
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    # Password reset
    # Password reset request page (user enters their email)
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    # Confirmation page telling the user that the password reset email has been sent
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    # Password reset link page (user arrives here after clicking the link in the email)
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # Password reset complete page (shows confirmation that password was successfully reset)
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
