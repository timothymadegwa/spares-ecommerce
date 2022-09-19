import re
from django import forms

class LoginForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(widget = forms.PasswordInput())

class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=20, required=True)
    last_name = forms.CharField(max_length=20, required=True)
    email = forms.EmailField(max_length=50, required=True)
    phone = forms.CharField(max_length=12, required=True)
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput())

class ShippingForm(forms.Form):
    shipping_name = forms.CharField(max_length=50, required=True)
    phone_number = forms.CharField(max_length=12, required=True)
    region = forms.CharField(max_length=20, required=True)
    shipping_location = forms.CharField(max_length=255, required=True)