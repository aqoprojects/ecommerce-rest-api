from django.shortcuts import render
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from .models import Product, Cart, Order, DeliveryOption
from .serializer import *
from django.contrib.auth.models import User
from django.db.models import F, Sum

# Create your views here.

class ProductListViewSet(viewsets.ModelViewSet):
  queryset = Product.objects.all()
  serializer_class = ProductsSerializer

class ProductCartViewSet(viewsets.ModelViewSet):
  queryset = Cart.objects.all()
  serializer_class = ProductCartSerializer

  def get_queryset(self):
    user = User.objects.first()
    return Cart.objects.filter(user=user, is_ordered=False)[:1]

  # def perform_create(self, serializer):
  #   user = User.objects.first()

  #   productId = serializer.validated_data.get('productId')
  #   quantity = serializer.validated_data.get('quantity', 1)

  #   existing_cart = Cart.objects.filter(user=user).exclude(cartNumber__isnull=True).first()
  #   userCartNumber = existing_cart.cartNumber if existing_cart else None
    
  #   defaults = {}
  #   if userCartNumber:
  #     defaults['cartNumber'] = userCartNumber

  #   cart, created = Cart.objects.get_or_create(
  #     user=user,
  #     productId=productId,
  #     cartNumber=userCartNumber,
  #     defaults=defaults
  #   )
  #   cart.quantity=quantity
  #   cart.save()

    # if not created:
    #   cart.quantity = F('quantity') + quantity
    #   cart.save()
    #   cart.refresh_from_db()
    # serializer.instance = cart

class CartProductsViewSet(viewsets.ModelViewSet):
  queryset = CartProduct.objects.all()
  serializer_class = CartProductSerializer

  def get_queryset(self):
    user = User.objects.first()
    return CartProduct.objects.filter(cartId__user=user, cartId__is_ordered=False)


  def perform_create(self, serializer):
    user = User.objects.first()

    productId = serializer.validated_data.get('productId')
    Quantity = serializer.validated_data.get('quantity', 1)

    cartNumber, created = Cart.objects.get_or_create(user=user, is_ordered=False)

    cart, created = CartProduct.objects.get_or_create(
      productId=productId,
      cartId=cartNumber,
      defaults={
      'quantity': Quantity,
      'total': productId.price * Quantity
    }
    )

    if not created:
      current_quantity = cart.quantity 
      cart.quantity = F('quantity') + Quantity
      cart.total =  (current_quantity + Quantity) * cart.productId.price
      cart.save()
      cart.refresh_from_db()
    serializer.instance = cart

  def perform_update(self, serializer):
    Quantity = serializer.validated_data.get('quantity', 1)

    serializer.save(
      total = serializer.insatce.productId.price * Quantity
    )
  

class ProductOrderViewSet(viewsets.ModelViewSet):
  queryset = Order.objects.all()
  serializer_class = ProductOrderSerializer

  def perform_create(self, serializer):
    user = User.objects.first()
    cart = Cart.objects.get(is_ordered=False)
    cartProducts = CartProduct.objects.filter(cartId=cart).aggregate(total_price=Sum('total'))
    
    newOrder = Order.objects.create(
      cartId=cart,
      total=cartProducts['total_price']
    )
    newOrder.save()
    cart.is_ordered = True
    cart.save()

    productId = Product.objects.first()

    cartNumber, created = Cart.objects.get_or_create(user=user, is_ordered=False)

    cart, created = CartProduct.objects.get_or_create(
      productId=productId,
      cartId=cartNumber,
      defaults={
      'quantity': 1,
      'total': productId.price * 1
    }
    )
    cart.save()


    serializer.instance = newOrder



class ProductDeliveryViewSet(viewsets.ModelViewSet):
  queryset = DeliveryOption.objects.filter(cartId__cartId__is_ordered=False)
  serializer_class = ProductDeliverySerializer

  def perform_update(self, serializer):
    deliveryDay = serializer.validated_data.get('deliveryDays', 7)
    deliveries = {
      "7":0,
      "3":3.00,
      "1":8.00
    }
    print(deliveryDay)
    print(type(deliveryDay))
    print(deliveries[deliveryDay])
    fee = deliveries[deliveryDay] if deliveryDay in deliveries else 0

    serializer.save(
      fee=fee
    )