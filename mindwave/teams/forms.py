from django import forms
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.contrib.auth import login, authenticate
from .models import Team
from accounts.models import Profile

class Create_team_form(forms.ModelForm):
    team_name = forms.CharField(max_length=100)
    members = forms.ModelMultipleChoiceField(queryset=Profile.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Team
        fields = ['team_name', 'members']
        
    def __init__(self, *args, **kwargs):
        super(Create_team_form, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Create Team'))
        
    def save(self, commit=True):
        team = super(Create_team_form, self).save(commit=False)
        if commit:
            team.save()
            self.save_m2m() 
        return team