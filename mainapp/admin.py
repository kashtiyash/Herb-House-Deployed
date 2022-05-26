from django.contrib import admin

# Register your models here.
from .models import Contact, Customer, Seller, Product, Order

admin.site.register(Contact)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(Product)
admin.site.register(Order)
