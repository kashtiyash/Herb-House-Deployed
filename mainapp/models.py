from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    message = models.CharField(max_length=500)

    def __str__(self):
        return self.email


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=12)
    profile_image = models.ImageField(null=True, upload_to="media/mainapp/images/", default="neuroly/profile_images"
                                                                                            "/default.jpg")

    def __str__(self):
        return self.user


class Seller(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=100, default="none")
    phone = models.CharField(max_length=12)
    profile_image = models.ImageField(null=True, upload_to="mainapp/images/",
                                      default="mainapp/images/")

    def __str__(self):
        return self.user.username


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)
    quantity = models.IntegerField(default=0)
    product_id = models.CharField(max_length=50)
    store_id = models.CharField(max_length=50)
    description = models.CharField(max_length=1000)
    product_image = models.ImageField(
        null=True, upload_to="mainapp/images", default="mainapp/images/M1_1.png")

    def __str__(self):
        return self.product_id


class Order(models.Model):
    order_id = models.CharField(max_length=50, unique=True)
    product_id = models.CharField(max_length=50)
    store_id = models.CharField(max_length=50)
    customer_id = models.CharField(max_length=50)
    quantity = models.IntegerField(default=0)
    customer_name = models.CharField(max_length=100, default="none")
    order_total = models.IntegerField(default=0)
    email = models.CharField(max_length=70)
    phone = models.CharField(max_length=12)
    address = models.CharField(max_length=300)

    razorpay_amount_total = models.IntegerField(default=0)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_pay_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_pay_sign = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.order_id, self.order_total
