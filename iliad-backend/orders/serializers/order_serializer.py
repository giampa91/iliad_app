from rest_framework import serializers
from orders.models.order import Order
from orders.models.product import Product
from orders.serializers.product_serializer import ProductSerializer

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True) 

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'description', 'date', 'products', 'version']
