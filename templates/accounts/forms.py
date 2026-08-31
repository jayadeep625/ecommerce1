from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Customer


class CustomerRegistrationForm(UserCreationForm):

    class Meta:
        model = Customer

        fields = [
            "username",
            "email",
            "password1",
            "password2",
        ]

    widgets = {
        "username": forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Username"
        }),

        "email": forms.EmailInput(attrs={
            "class": "form-control",
            "placeholder": "Enter Email"
        }),
    }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields["username"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Username"
        })

        self.fields["email"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Email Address"
        })

        self.fields["password1"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Password"
        })

        self.fields["password2"].widget.attrs.update({
            "class": "form-control",
            "placeholder": "Confirm Password"
        })