from django import forms
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class GPTRequestForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    
    
    def __init__(self, *args, **kwargs):
        super(GPTRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Generate Text'))
