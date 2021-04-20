from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class User(AbstractUser):
    email = models.EmailField("email", unique=True, blank=False)
    deliv_address_street = models.CharField(blank=False, max_length=256)
    deliv_address_houseno = models.CharField(blank=False, max_length=10)
    deliv_address_zipcode = models.CharField(blank=False, max_length=5)
    deliv_address_city = models.CharField(blank=False, max_length=30)
    deliv_address_country = models.CharField(blank=False, max_length=30, default="Germany")

class Category(models.Model):
    name = models.CharField(blank=False, max_length=20)
    description = models.TextField(blank=False)
    display_order = models.PositiveSmallIntegerField(default=False)
    is_active = models.BooleanField(default=False)


