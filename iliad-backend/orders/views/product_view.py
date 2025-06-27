from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from orders.models.product import Product
from orders.serializers.product_serializer import ProductSerializer

class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            raise NotFound(detail="Product not found")
        serializer = ProductSerializer(product)
        return Response(serializer.data)
