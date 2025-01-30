from rest_framework import serializers

from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.Name", read_only=True)
    product_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="product.Price", read_only=True
    )
    product_image = serializers.ImageField(source="product.Image", read_only=True)
    product_weight = serializers.CharField(source="product.Weight", read_only=True)

    class Meta:
        model = CartItem
        fields = (
            "product_name",
            "quantity",
            "item_subtotal",
            "product_price",
            "product_image",
            "product_weight",
            "id",
            "product",
        )


class CartSerializer(serializers.ModelSerializer):
    cartitems = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="total")

    def total(self, obj):
        cart_Items = obj.cartitems.all()
        return sum(Item.item_subtotal for Item in cart_Items)

    class Meta:
        model = Cart
        fields = ("user", "cartitems", "total_price")
