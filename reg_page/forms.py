from django import forms
from django.contrib.auth.models import User

class UsernameForm(forms.ModelForm):
    username = forms.CharField(required=False)

    class Meta:
        model = User
        fields = ['username']

