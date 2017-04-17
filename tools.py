from django import forms

class RegisterForm(forms.Form):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField()

class LoginForm(forms.Form):
    username =forms.CharField()
    password =forms.CharField()
