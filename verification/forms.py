# verification/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SignatureUpload

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class UploadForm(forms.ModelForm):
    class Meta:
        model = SignatureUpload
        fields = ['image']
