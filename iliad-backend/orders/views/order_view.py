from rest_framework import viewsets, status
from rest_framework.response import Response
from orders.models.order import Order
from orders.serializers.order_serializer import OrderSerializer
from orders.serializers.order_update_serializer import OrderUpdateSerializer
from orders.serializers.order_create_serializer import OrderCreateSerializer
from orders.serializers.simple_product_input_serializer import SimpleProductInputSerializer
from orders.services.order_service import OrderService
from rest_framework.viewsets import ModelViewSet
from orders.pagination import CustomPageNumberPagination

class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    pagination_class = CustomPageNumberPagination
    order_service = OrderService()

    def list(self, request):
        filters = {
            "search": request.query_params.get("search"),
            "date_start": request.query_params.get("date_start"),
            "date_end": request.query_params.get("date_end"),
        }
        orders = self.order_service.list_orders(filters)
        page = self.paginate_queryset(orders)
        if page is not None:
            serializer = OrderSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        order = self.order_service.get_order(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def create(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            order = self.order_service.create_order(serializer.validated_data) 
            response_serializer = OrderSerializer(order)
            return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        pk = kwargs.get('pk')  # get the order id
        input_serializer = OrderUpdateSerializer(data=request.data, partial=partial)
        input_serializer.is_valid(raise_exception=True)
        updated_order = self.order_service.update_order(pk, input_serializer.validated_data)
        output_serializer = OrderSerializer(updated_order)
        return Response(output_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        order = self.order_service.get_order(pk)
        self.order_service.delete_order(order)
        return Response(status=status.HTTP_204_NO_CONTENT)
