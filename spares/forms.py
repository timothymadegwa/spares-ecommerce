from django import forms

class ShippingForm(forms.Form):
    shipping_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=50, required=False)
    phone_number = forms.CharField(max_length=12, required=True)
    region = forms.CharField(max_length=20, required=True)
    shipping_location = forms.CharField(max_length=255, required=True)