from django.db.models.base import Model
from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        # fields = '__all__'
        exclude = ['vote_total', 'vote_ratio']