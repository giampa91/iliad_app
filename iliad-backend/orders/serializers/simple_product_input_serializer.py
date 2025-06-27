from rest_framework import serializers
from orders.models.order import Order
from orders.models.product import Product
from orders.serializers.product_serializer import ProductSerializer

class SimpleProductInputSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, allow_null=True)
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)
