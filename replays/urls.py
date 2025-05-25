from django.urls import path
from . import views

app_name = 'replies'

urlpatterns = [
    path('add/<int:comment_id>/', views.add_reply, name='add_reply'),
    path('edit/<int:reply_id>/', views.edit_reply, name='edit_reply'),
    path('delete/<int:reply_id>/', views.delete_reply, name='delete_reply'),
    path('api/comment/<int:comment_id>/', views.get_comment_replies, name='get_comment_replies'),
]