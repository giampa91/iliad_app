# order.py
from django.db import models
from django.utils import timezone

class Order(models.Model):
    customer_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    date = models.DateTimeField(default=timezone.now)
    version = models.PositiveIntegerField(default=0)


    def __str__(self):
        return f"Order {self.id} - {self.customer_name}"
