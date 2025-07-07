from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Sum
from .models import Product, Cart, Order, DeliveryOption, CartProduct

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username','first_name', 'last_name']


class ProductsSerializer(serializers.ModelSerializer):
  class Meta:
    model = Product
    fields = '__all__'


class ProductDeliverySerializer(serializers.ModelSerializer):

  class Meta:
    model = DeliveryOption
    fields = ['id', 'deliveryDays', 'fee']

class CartProductSerializer(serializers.ModelSerializer):
  product = ProductsSerializer(source="productId", read_only=True)
  delivery = ProductDeliverySerializer(source='cartdevlivery', many=True, read_only=True)
  class Meta:
    model = CartProduct
    fields = ['id', 'productId', 'total' ,'quantity',  'product', 'delivery']
    read_only_fields = ['total','overall_total', 'delivery']
  
  # def get_overall_total(self, obj):
  #   cart = obj.cartId
  #   delivery_total = DeliveryOption.objects.filter(
  #       cartId__cartId__is_ordered=False
  #   ).aggregate(delivery_total=Sum('fee'))['delivery_total'] or 0.0
  #   cart_total = CartProduct.objects.filter(
  #       cartId=cart,
  #       cartId__is_ordered=False
  #   ).aggregate(cart_total=Sum('total'))['cart_total'] or 0.0
  #   return float(delivery_total) + float(cart_total)


class ProductCartSerializer(serializers.ModelSerializer):
  user = UserSerializer(read_only=True) 
  cartproducts = CartProductSerializer(source="cartid", many=True, read_only=True)
  overall_total = serializers.SerializerMethodField()
  cart_product_total = serializers.SerializerMethodField()
  delivery_fee_total = serializers.SerializerMethodField()
  class Meta:
    model = Cart
    fields = ['id', 'overall_total', 'cart_product_total', 'delivery_fee_total', 'user', 'cartNumber', 'cartproducts']
    read_only_fields = ['cartNumber', 'user', 'cartproducts']

  def get_overall_total(self, obj):
    cart = obj
    delivery_total = DeliveryOption.objects.filter(
        cartId__cartId__is_ordered=False
    ).aggregate(delivery_total=Sum('fee'))['delivery_total'] or 0.0
    cart_total = CartProduct.objects.filter(
        cartId=cart,
        cartId__is_ordered=False
    ).aggregate(cart_total=Sum('total'))['cart_total'] or 0.0
    return float(delivery_total) + float(cart_total)
  
  def get_cart_product_total(self, obj):
    cart = obj
    cart_total = CartProduct.objects.filter(
        cartId=cart,
        cartId__is_ordered=False
    ).aggregate(cart_total=Sum('total'))['cart_total'] or 0.0
    return cart_total
  
  def get_delivery_fee_total(self, obj):
    cart = obj
    delivery_total = DeliveryOption.objects.filter(
        cartId__cartId__is_ordered=False
    ).aggregate(delivery_total=Sum('fee'))['delivery_total'] or 0.0
    
    return delivery_total

class ProductOrderSerializer(serializers.ModelSerializer):
  cart = ProductCartSerializer(source="cartId", read_only=True)
  class Meta:
    model = Order
    fields = ['id','total','cartId', 'cart']
