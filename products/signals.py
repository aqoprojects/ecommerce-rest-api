from django.db.models.signals import post_save, pre_save
from django.dispatch.dispatcher import receiver
from .models import Order, DeliveryOption, CartProduct
from django.db.models import Sum

@receiver(post_save, sender=CartProduct)
def updateCart(sender, instance, created, **kwargs):
  if created:
    DeliveryOption.objects.create(
      cartId=instance,
    )
  