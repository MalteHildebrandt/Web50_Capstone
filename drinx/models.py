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

    def __str__(self):
        return f"{self.name}"

class Image(models.Model):
    image_large = models.ImageField(upload_to='images', blank=False)


class Article(models.Model):
    name = models.CharField(blank=False, max_length=20)
    description_short = models.CharField(blank=False, max_length=30)
    description = models.TextField(blank=False)
    image = models.ImageField(upload_to='images/articles', blank=False)
    categories = models.ManyToManyField("Category", blank = False, related_name="articles")
    content_qty = models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    content_qty_unit = models.ForeignKey("ContentUnit", blank=False, on_delete=models.RESTRICT)
    package_qty = models.PositiveSmallIntegerField(default=False)
    price =  models.DecimalField(blank=False, max_digits=5, decimal_places=2)
    stock = models.PositiveSmallIntegerField(default=False)
    is_active = models.BooleanField(blank=False, default=False)
    
    def __str__(self):
        return f"{self.id}"
    

class ContentUnit(models.Model):
    name = models.CharField(blank=False, max_length=3)
    description = models.CharField(blank=False, max_length=20, default='')

    def __str__(self):
        return f"{self.description}"

