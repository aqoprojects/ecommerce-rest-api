from django.db import models
import uuid 
from products.models.ProductModel import Product
from django.contrib.auth.models import User

class Cart(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
  cartNumber = models.UUIDField(default=uuid.uuid4)
  is_ordered = models.BooleanField(default=False)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  class Meta: 
    unique_together = [['user', 'cartNumber']]

  def __str__(self):
    return f"{self.user.username} - cart number: {self.cartNumber}"