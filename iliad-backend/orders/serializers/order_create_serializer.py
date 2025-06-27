from rest_framework import serializers
from orders.models.order import Order
from orders.models.product import Product
from orders.serializers.product_serializer import ProductSerializer

class OrderCreateSerializer(serializers.ModelSerializer):
    description = serializers.CharField(required=True)
    date = serializers.DateTimeField(required=True)
    class Meta:
        model = Order
        fields = ['customer_name', 'description', 'date'] 

