from django import forms




class AdminLoginForm(forms.Form):
    username= forms.CharField(widget=forms.TextInput())
    password= forms.CharField(widget=forms.PasswordInput())

