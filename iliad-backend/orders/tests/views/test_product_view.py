from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from orders.models.product import Product
from orders.tests.factories import ProductFactory

class ProductViewSetTest(APITestCase):

    def setUp(self):
        # Create some products for testing list and retrieve
        self.product1 = ProductFactory(name="Product 1", price=10)
        self.product2 = ProductFactory(name="Product 2", price=20)

    def test_list_products(self):
        url = reverse('product-list')  # expects router with basename='product'
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.product1.name)
        self.assertEqual(response.data[1]['name'], self.product2.name)

    def test_retrieve_product_success(self):
        url = reverse('product-detail', args=[self.product1.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.product1.id)
        self.assertEqual(response.data['name'], self.product1.name)

    def test_retrieve_product_not_found(self):
        url = reverse('product-detail', args=[99999])  # non-existing id
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Product not found")
