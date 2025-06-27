from django.test import TestCase
from orders.serializers.product_serializer import ProductSerializer
from decimal import Decimal

class ProductSerializerTest(TestCase):

    def test_valid_data_without_id(self):
        data = {
            'name': 'Test Product',
            'price': '9.99'  # can also be string, DRF will convert it to Decimal
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['price'], Decimal('9.99'))  # Compare with Decimal

    def test_valid_data_with_id(self):
        data = {
            'id': 1,
            'name': 'Existing Product',
            'price': '19.99'
        }
        serializer = ProductSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['price'], Decimal('19.99'))  # Use Decimal here

    def test_invalid_missing_name(self):
        data = {
            'price': 5.00
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)

    def test_invalid_price_type(self):
        data = {
            'name': 'Invalid Price Product',
            'price': 'not a number'
        }
        serializer = ProductSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('price', serializer.errors)
