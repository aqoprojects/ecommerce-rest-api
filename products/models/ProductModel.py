from django.db import models
import uuid


class Product(models.Model):
  id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
  image = models.ImageField(upload_to='product_image/', null=True, blank=True )
  name = models.CharField(max_length=70)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  keywords = models.CharField(max_length=100)
  created_date = models.DateTimeField(auto_now_add=True)
  updated_date = models.DateTimeField(auto_now=True)