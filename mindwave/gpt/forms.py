from django import forms
from django.db import models
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from base.models import Subject

class GPTRequestForm(forms.Form):
    prompt = forms.CharField(widget=forms.Textarea(attrs={'rows': 5, 'cols': 100}))
    
    
    def __init__(self, *args, **kwargs):
        super(GPTRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Generate Text'))


class GPTQuizForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Subject.objects.all())
    questions_count = forms.IntegerField(initial=5)
    answers_count = forms.IntegerField(initial=2, min_value=2, max_value=5)
    mixed_answers_count = forms.BooleanField(required=False, initial=False, label="Mixed Answers Count")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.add_input(Submit('submit', 'Submit'))
    
    def clean(self):
        cleaned_data = super().clean()
        questions_count = cleaned_data.get("questions_count")
        answers_count = cleaned_data.get("answers_count")
        
        if questions_count and answers_count:
            if answers_count >= questions_count:
                raise forms.ValidationError("Answers count should be less than questions count")
        
        return cleaned_data
    
    def save(self):
        return self.cleaned_data
