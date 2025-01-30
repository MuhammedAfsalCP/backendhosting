from django.db import models

from products.models import Products
from users.models import User

# Create your models here.

#TODO-indexing
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    address = models.JSONField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        indexes = [
            models.Index(fields=['user']),  # Index for user field
            models.Index(fields=['order_id']),  # Index for order_id field
            models.Index(fields=['created_at']),  # Index for created_at field
        ]

    def __str__(self):
        return f"Order {self.order_id} by {self.user.username}"

class OrderItem(models.Model):
    class StatusChoices(models.TextChoices):
        SHIPPING = "Shipping"
        CANCELLED = "Cancelled"
        RETURNED = "Returned"
        DELIVERED = "Delivered"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(
        max_length=10, choices=StatusChoices.choices, default=StatusChoices.SHIPPING
    )

    class Meta:
        indexes = [
            models.Index(fields=['order']),  # Index for order field
            models.Index(fields=['status']),  # Index for status field
        ]

    @property
    def item_subtotal(self):
        return self.product.Price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.Name} in order {self.order.order_id}"
