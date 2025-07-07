from django.urls import path, include
from products.views import ProductListViewSet, ProductCartViewSet, ProductOrderViewSet, CartProductsViewSet, ProductDeliveryViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductListViewSet, basename="products")
router.register(r'product-cart', ProductCartViewSet, basename="product-cart")
router.register(r'product-order', ProductOrderViewSet, basename="product-order")
router.register(r'cart-product', CartProductsViewSet, basename="cart-Product")
router.register(r'product-delivery', ProductDeliveryViewSet, basename="Product-delivery")


urlpatterns = [
  path('', include(router.urls))
]