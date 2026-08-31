from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):

    ROLE_CHOICES = (
        ("CUSTOMER", "Customer"),
        ("SELLER", "Seller"),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default="CUSTOMER"
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    def __str__(self):
        return self.username


class UserProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to="profiles/",
        default="profiles/default.png"
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    address = models.TextField(
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    state = models.CharField(
        max_length=100,
        blank=True
    )

    pincode = models.CharField(
        max_length=10,
        blank=True
    )

    def __str__(self):
        return self.user.username