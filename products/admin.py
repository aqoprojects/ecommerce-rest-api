from django.contrib import admin
from .models import Product, Cart, CartProduct, Order, DeliveryOption

admin.site.register([Product, Cart, CartProduct ,Order, DeliveryOption])