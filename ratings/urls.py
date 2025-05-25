from django.urls import path
from . import views

app_name = 'ratings'

urlpatterns = [
    path('add/<int:project_id>/', views.add_rating, name='add_rating'),
    path('get/<int:project_id>/', views.get_project_ratings, name='get_ratings'),
]