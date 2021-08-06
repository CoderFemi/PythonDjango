from django.db.models.base import Model
from django.forms import ModelForm, widgets
from django import forms
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__'
        exclude = ['owner', 'vote_total', 'vote_ratio']
        widgets = {
            'tags': forms.CheckboxSelectMultiple()
        }
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder': 'Add title'})

        for (name, field) in self.fields.items():
            field.widget.attrs.update({'class':'input'})