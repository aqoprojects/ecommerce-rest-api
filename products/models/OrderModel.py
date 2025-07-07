from django.db import models
import uuid 
from products.models.CartModel import Cart
from django.contrib.auth.models import User

class Order(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  cartId = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart')
  total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)