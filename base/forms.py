from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Discussion,User
from django.core.exceptions import ValidationError
from datetime import date


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email','birth_date', 'password1', 'password2']
        widgets = {
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date')
        if birth_date:
            age = (date.today() - birth_date).days // 365
            if age < 18:
                raise ValidationError("Age must be 18 years or older.")

        


class DiscussionForm(ModelForm):
    class Meta:
        model = Discussion 
        fields = ['title', 'content']

        
class EditUser(ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','github','bio','birth_date','location','gender','Use_code','display_notification']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-Settings'}),
            'last_name': forms.TextInput(attrs={'class': 'form-Settings'}),
            'bio': forms.Textarea(attrs={'class': 'form-Settings bio-Settings '}),
            'birth_date': forms.DateInput(attrs={'class': 'form-Settings', 'type': 'date'}),
            'location': forms.TextInput(attrs={'class': 'form-Settings'}),
            'gender': forms.Select(attrs={'class': 'form-Settings'}),
            'display_notification': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'github': forms.TextInput(attrs={'class': 'form-Settings'}),
            'Use_code': forms.TextInput(attrs={'class': 'form-Settings'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        birth_date = cleaned_data.get('birth_date')
        if birth_date:
            age = (date.today() - birth_date).days // 365
            if age < 18:
                raise ValidationError("Age must be 18 years or older.", code='invalid', params={})

class EditPortfolio(ModelForm):
    class Meta:
        model = User
        fields = ['portfolio']
        widgets = {
            'portfolio': forms.Textarea(attrs={'class': 'portfolio'}),
        }