# product.py
from django.db import models

class Product(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name
