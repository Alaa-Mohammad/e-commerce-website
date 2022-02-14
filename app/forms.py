from django import forms
from django.contrib.auth.forms import (UserCreationForm,UsernameField,AuthenticationForm,PasswordChangeForm,
PasswordResetForm,SetPasswordForm)
from django.contrib.auth.models import User
from django.http import request
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from app.models import Customer

class RegistrationForm(UserCreationForm):
    email= forms.CharField(required=True,widget=forms.EmailInput(attrs={'class':'form-control'}),label='Email')
    password1 = forms.CharField(
    label=_("Password"),
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    help_text=password_validation.password_validators_help_text_html(),
     )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        )
    class Meta:
        model = User
        fields = ("username","email",'password1','password2')
        field_classes = {'username': UsernameField}
        widgets={
            'username':forms.TextInput(attrs={'class':'form-control'}),}
        
class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True,'class':'form-control'}))
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password','class':'form-control'}),
    )        
        
class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
    label=_("Old password"),
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'autofocus': True,'class':'form-control'}),
    )   
    new_password1 = forms.CharField(
    label=_("New Password"),
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    help_text=password_validation.password_validators_help_text_html(),
     )
    new_password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        ) 

class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email','class':'form-control'})
    )    

class SetPassword_Form(SetPasswordForm): 
    new_password1 = forms.CharField(
    label=_("New Password"),
    strip=False,
    widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
    help_text=password_validation.password_validators_help_text_html(),
     )
    new_password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password','class':'form-control'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
        )     

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Customer
        fields=('name','locality','city','state','zipcode')
        widgets={
            'name':forms.TextInput(attrs={'class':'form-control'}),
            'locality':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.Select(attrs={'class':'form-control'}),
            'zipcode':forms.NumberInput(attrs={'class':'form-control'}),
            }
  


