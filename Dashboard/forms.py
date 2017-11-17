from django import forms
from django.forms import ValidationError
from .models import User
from django.contrib.auth import authenticate

class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password')

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        if not user or not user.is_active:
            raise ValidationError("Incorrect username or password :(")
        return self.cleaned_data

    def login(self, request):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        user = authenticate(username=username, password=password)
        return user

class SignupForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('username', 'email', 'password')
