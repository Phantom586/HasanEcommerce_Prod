from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    full_name = forms.CharField(max_length=100)
    phone_no = forms.CharField(max_length=13)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'email', 'phone_no', 'password1', 'password2']