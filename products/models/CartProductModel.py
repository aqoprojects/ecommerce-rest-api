from django.db import models
import uuid 
from products.models.ProductModel import Product
from products.models.CartModel import Cart
from django.contrib.auth.models import User

class CartProduct(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  productId = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product')
  cartId = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cartid')
  quantity = models.IntegerField(default=1)
  total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)

  class Meta: 
    unique_together = [['cartId', 'productId']]

  # def save(self):
  #   if self.productId:
  #     quanity = self.quantity
  #     productPrice = self.productId.price
  #     self.total = productPrice * quanity
  #   return super().save()

  
  

  def __str__(self):
    return f"cart number: {self.cartId.cartNumber} - {self.productId.name} - {self.cartId.user.username}"