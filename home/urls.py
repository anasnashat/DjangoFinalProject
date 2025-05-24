from django.urls import path
from . import views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('search/', views.search_results, name='search_results'),
    path('category/<int:category_id>/', views.category_projects, name='category_projects'),

]
