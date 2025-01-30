import re

from rest_framework import serializers

from cart.serialzer import CartSerializer
from orders.serializer import OrderSerializer

from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "password",
            "password2",
        )

    def validate(self, attrs):
        password = attrs.get("password")
        password2 = attrs.get("password2")

        # Check if password and password2 match

        # Validate password strength
        if len(password) < 8:
            raise serializers.ValidationError(
                {"password": "Password must be at least 8 characters long."}
            )

        if not re.search(r"[A-Za-z]", password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one alphabetic character."}
            )

        if not re.search(r"[0-9]", password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one numeric character."}
            )

        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise serializers.ValidationError(
                {"password": "Password must contain at least one special character."}
            )
        if password != password2:
            raise serializers.ValidationError({"Error": "Passwords do not match."})

        return attrs


class UserVerificatioSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "password")

    def save(self):
        # This method is responsible for saving the user
        password = self.validated_data["password"]

        # Create the User object without saving it yet
        account = User(
            email=self.validated_data["email"],
            username=self.validated_data["username"],
            first_name=self.validated_data["first_name"],
            last_name=self.validated_data["last_name"],
        )

        # Set the password (hash it)
        account.set_password(password)

        # Save the account object to the database
        account.save()

        return account  # Optionally return the saved user object


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "is_staff")


class AdminShowSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "is_active", "id")


class UserAllDetailsSerializer(serializers.ModelSerializer):
    cart = CartSerializer()
    orders = OrderSerializer(many=True)

    class Meta:
        model = User
        fields = ("username", "email", "is_active", "cart", "orders")
