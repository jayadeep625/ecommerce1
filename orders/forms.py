from django import forms
from .models import Address

class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        fields = [
            "full_name",
            "phone",
            "email",
            "house",
            "street",
            "city",
            "state",
            "pincode",
        ]

        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Full Name"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone Number"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email Address"}),
            "house": forms.TextInput(attrs={"placeholder": "House / Flat No"}),
            "street": forms.TextInput(attrs={"placeholder": "Street"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "state": forms.TextInput(attrs={"placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"placeholder": "Pincode"}),
        }