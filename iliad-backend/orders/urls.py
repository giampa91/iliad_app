from django.urls import path, include
from rest_framework.routers import DefaultRouter
from orders.views.order_view import OrderViewSet
from orders.views.product_view import ProductViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
