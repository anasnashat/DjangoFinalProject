from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('add/<int:project_id>/', views.add_comment, name='add_comment'),
    path('edit/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('delete/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('api/project/<int:project_id>/', views.get_project_comments, name='get_project_comments'),
]