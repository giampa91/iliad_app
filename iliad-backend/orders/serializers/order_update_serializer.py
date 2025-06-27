from rest_framework import serializers
from orders.models.order import Order
from orders.models.product import Product
from orders.serializers.simple_product_input_serializer import SimpleProductInputSerializer

class OrderUpdateSerializer(serializers.ModelSerializer):
    products = SimpleProductInputSerializer(many=True)
    products_to_delete = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    version = serializers.IntegerField()


    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'description', 'date', 'products', 'products_to_delete', 'version']

    def update(self, instance, validated_data):
        order_service = OrderService()
        updated_order = order_service.update_order(instance, validated_data)

        return updated_order
