from django.db import models

from products.models import Products
from users.models import User

# Create your models here.


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=['user']),  # Index for user field
            models.Index(fields=['created_at']),  # Index for created_at field (optional)
        ]

    def __str__(self):
        return f"{self.user.username}'s Cart"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cartitems")
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        indexes = [
            models.Index(fields=['cart']),  # Index for cart field
            models.Index(fields=['product']),  # Index for product field
        ]

    @property
    def item_subtotal(self):
        return self.product.Price * self.quantity

    def __str__(self):
        return f"{self.quantity} of {self.product} from {self.cart.user.username}'s Cart"
