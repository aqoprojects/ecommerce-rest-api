from django.db import models
import uuid 
from products.models.ProductModel import Product
from django.contrib.auth.models import User
from products.models.CartProductModel import CartProduct


class DeliveryOption(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  cartId = models.ForeignKey(CartProduct, on_delete=models.CASCADE, unique=True, related_name='cartdevlivery')
  deliveryDays = models.CharField(max_length=10, choices=[('7', '7 days'), ('3', '3 days'), ('1', '1 Day')], default='7')
  fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)


  # def save(self):
  #   if self.deliveryDays == '7':
  #     self.fee = 0
  #   elif self.deliveryDays == '3':
  #     self.fee = 3.00
  #   elif self.deliveryDays == '1':
  #     self.fee = 8.00
  #   return super().save()

  def __str__(self):
    return f' {self.cartId} - {self.deliveryDays}'
  
  