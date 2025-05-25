from django.urls import path
from .views import create_report, report_list 

urlpatterns = [
    path('report/', create_report, name='create_report'),
    path('reports/', report_list, name='report_list'),
]