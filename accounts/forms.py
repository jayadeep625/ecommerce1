from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from .models import UserProfile


class CustomerRegistrationForm(UserCreationForm):

    email = forms.EmailField(required=True)

    class Meta:
        model = User

        fields = [
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "password1",
            "password2",
        ]

    def save(self, commit=True):
        user = super().save(commit=False)

        # Registration page creates customers only
        user.role = "CUSTOMER"

        if commit:
            user.save()

        return user

class ProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile

        fields = [
            "profile_image",
            "phone",
            "address",
            "city",
            "state",
            "pincode",
        ]