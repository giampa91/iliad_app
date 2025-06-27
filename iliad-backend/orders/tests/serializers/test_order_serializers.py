from django.test import TestCase
from datetime import date
from orders.models.order import Order
from orders.models.product import Product
from orders.serializers.order_update_serializer import OrderUpdateSerializer

class OrderUpdateSerializerTestCase(TestCase):
    def setUp(self):
        # Create an order instance for testing
        self.order = Order.objects.create(
            customer_name='John Doe',
            description='Sample order',
            date=date.today()
        )
        # Create two products related to the order
        self.product1 = Product.objects.create(order=self.order, name='Product 1', price=10)
        self.product2 = Product.objects.create(order=self.order, name='Product 2', price=20)

    def test_valid_data(self):
        update_data = {
            'customer_name': 'John Smith',
            'description': 'Updated order',
            'date': '2025-06-29',
            'products': [
                {'id': self.product1.id, 'name': 'Updated Product 1', 'price': '15.00'},
                {'name': 'New Product', 'price': '30.00'}
            ],
            'products_to_delete': [self.product2.id],
            'version': 0
        }
        
        serializer = OrderUpdateSerializer(instance=self.order, data=update_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)

        validated_data = serializer.validated_data
        self.assertEqual(validated_data['customer_name'], 'John Smith')
        self.assertEqual(validated_data['description'], 'Updated order')
        self.assertEqual(validated_data['date'].date().isoformat(), '2025-06-29')

        products = validated_data['products']
        self.assertEqual(len(products), 2)
        self.assertEqual(products[0]['name'], 'Updated Product 1')
        self.assertEqual(products[1]['name'], 'New Product')

        products_to_delete = validated_data.get('products_to_delete', [])
        self.assertIn(self.product2.id, products_to_delete)

    def test_missing_required_field(self):
        # Assuming 'customer_name' is required by your model or serializer
        update_data = {
            'description': 'Updated order',
            'date': '2025-06-29',
            'products': [],
        }
        serializer = OrderUpdateSerializer(instance=self.order, data=update_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('customer_name', serializer.errors)

    def test_invalid_products_to_delete_type(self):
        update_data = {
            'customer_name': 'John Smith',
            'description': 'Updated order',
            'date': '2025-06-29',
            'products': [],
            'products_to_delete': ['not-an-int', 3.5]
        }
        serializer = OrderUpdateSerializer(instance=self.order, data=update_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('products_to_delete', serializer.errors)

    def test_invalid_product_data(self):
        # Missing price in one product, which is required by SimpleProductInputSerializer
        update_data = {
            'customer_name': 'John Smith',
            'description': 'Updated order',
            'date': '2025-06-29',
            'products': [
                {'name': 'Product without price'}
            ],
            'products_to_delete': []
        }
        serializer = OrderUpdateSerializer(instance=self.order, data=update_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('products', serializer.errors)

    def test_empty_products_and_products_to_delete(self):
        update_data = {
            'customer_name': 'John Smith',
            'description': 'Updated order',
            'date': '2025-06-29',
            'products': [],
            'products_to_delete': [],
            'version' : 1
        }
        serializer = OrderUpdateSerializer(instance=self.order, data=update_data)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        self.assertEqual(serializer.validated_data['products'], [])
        self.assertEqual(serializer.validated_data['products_to_delete'], [])