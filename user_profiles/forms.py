from django import forms
from django.contrib.auth.models import User
from user_profiles.models import Profile

class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    
    class Meta:
        model = Profile
        fields = ['image', 'country', 'phone_number', 'address', 'birthdate', 'gender'] # can add facebook_profile -bonus-
        widgets = {
            'birthdate': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and hasattr(self.instance, 'user'):
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        
        user = profile.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            profile.save()
        
        return profile