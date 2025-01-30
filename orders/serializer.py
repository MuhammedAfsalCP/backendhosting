from rest_framework import serializers

from products.serializer import ProductsSeriealizer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductsSeriealizer()

    class Meta:
        model = OrderItem
        fields = ("product", "quantity", "status", "item_subtotal", "id")


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True, source="items")

    class Meta:
        model = Order
        fields = ("order_id", "created_at", "orderitems", "address", "total_price")


class AllOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ("order_id", "created_at", "total_price", "id")
