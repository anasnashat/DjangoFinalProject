from django import forms
from .models import Reply

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['replay']
        widgets = {
            'replay': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Write your reply here...',
                'required': True
            })
        }
        labels = {
            'replay': ''
        }