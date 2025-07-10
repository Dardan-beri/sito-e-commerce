from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    address = forms.CharField(widget=forms.Textarea, required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'address', 'password1', 'password2')

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'