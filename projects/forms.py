from django import forms
from django.core.exceptions import ValidationError
from .models import Project, ProjectImage
from django.forms import modelformset_factory
from django.forms import inlineformset_factory
from .models import Project, ProjectImage
class ProjectForm(forms.ModelForm):
    starting_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    ending_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    class Meta:
        model = Project
        fields = ['title', 'details', 'total_target', 'starting_date', 
                  'ending_date', 'is_active', 'category', 'tags', 'is_featured']
        exclude = ['created_by']  
        widgets = {
            'details': forms.Textarea(attrs={'rows': 4}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        starting_date = cleaned_data.get('starting_date')
        ending_date = cleaned_data.get('ending_date')
                
        if starting_date and ending_date and ending_date < starting_date:
            raise ValidationError("Ending date cannot be before the starting date.")
        return cleaned_data

class ProjectImageForm(forms.ModelForm):
    class Meta:
        model = ProjectImage
        fields = ['image'] 

ProjectImageFormSet = inlineformset_factory(
    Project, ProjectImage, form=ProjectImageForm,
    fields=['image'], extra=1, can_delete=True
)
