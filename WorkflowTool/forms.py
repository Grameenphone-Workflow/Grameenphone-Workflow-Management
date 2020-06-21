from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import GPUser

from django import forms

class LoginForm(forms.Form):
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'phone_number',
            'value': '',
            'placeholder': 'Enter Phone Number',
        })
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'name': 'password',
            'value': '',
            'placeholder': 'Password',
        })
    )

class OnboardingForm(forms.Form):
    
    # This is the full corporate customer name.
    corporate_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'corporate_name',
            'value': '',
            'placeholder': 'BATA Something',
        })
    )

    # Shorter ver. of the corporate customer name.
    corporate_short_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'corporate_short_name',
            'value': '',
            'placeholder': 'BATA_SOMETHING',
        })
    )

    bs_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'name': 'bs_code',
        })
    )