from rest_framework import serializers
from orders.models.product import Product

class ProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False, allow_null=False)

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']