"""
URL configuration for final_project projects.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from donation_project import settings
from django.http import HttpResponse

def temporary_login_view(request):
    return HttpResponse("Login page placeholder")

urlpatterns = [
    path('',include('home.urls')),
    path('login/', temporary_login_view, name='login'),
    path('admin/', admin.site.urls),
    path('projects/', include('projects.urls')),
    path('payments/', include('payments.urls')),
    path('donations/', include('donations.urls',namespace='donations')),
    path('profiles/', include('user_profiles.urls')),
    path('users/', include('users.urls'))
]



if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
