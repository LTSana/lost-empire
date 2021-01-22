from django.contrib import admin

# Register your models here.

# Import Models
from .models import Products, Orders, CouponCodes

admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(CouponCodes)
