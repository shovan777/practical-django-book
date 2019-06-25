from django.db import models
from .managers import ActiveManager, ProductTagManager, UserManager

from django.contrib.auth.models import (
    AbstractUser
)
# Create your models here.


class ProductTag(models.Model):
    objects = ProductTagManager()
    name = models.CharField(max_length=32)
    slug = models.SlugField(max_length=48)
    description = models.TextField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.slug, )


class Product(models.Model):
    objects = ActiveManager()

    tags = models.ManyToManyField(ProductTag,
                                  blank=True)
    name = models.CharField(max_length=32)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=6,
                                decimal_places=2)
    slug = models.SlugField(max_length=48)
    active = models.BooleanField(default=True)
    in_stock = models.BooleanField(default=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    # name = models.CharField(max_length=32)

    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to="product-images"
    )
    thumbnail = models.ImageField(
        upload_to="product-thumbnails", null=True
    )

    def __str__(self):
        return self.product.name


# class ProductTag(models.Model):
#     name = models.CharField(max_length=32)
#     slug = models.SlugField(max_length=48)
#     description = models.TextField(blank=True)
#     active = models.BooleanField(default=True)

#     def __str__(self):
#         return self.name

#     def natural_key(self):
#         return (self.slug, )

class User(AbstractUser):
    username = None
    email = models.EmailField('email address',
                              unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()


class Address(models.Model):
    SUPPORTED_COUNTRIES = (
        ("uk", "United Kingdom"),
        ("us", "United States of America"),
        ("np", "Nepal"),
    )
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    address1 = models.CharField("Address line 1",
                                max_length=60)
    address2 = models.CharField(
        "Address line 2", max_length=60, blank=True
    )
    zip_code = models.CharField(
        "ZIP / Postal code", max_length=12
    )
    city = models.CharField(max_length=60)
    country = models.CharField(
        max_length=3, choices=SUPPORTED_COUNTRIES
    )

    def __str__(self):
        return ", ".join(
            [
                self.name,
                self.address1,
                self.address2,
                self.zip_code,
                self.city,
                self.country,
            ]
        )
