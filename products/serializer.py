from rest_framework import serializers
from .models import Products
from .utils import upload_image_to_s3

class ProductsSeriealizer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = (
            "id",
            "Name",
            "Category",
            "Price",
            "Description",
            "Brand",
            "Weight",
            "Stock",
            "Image",
            "Ingredient",
        )
        

    # Validate Product Name
    def validate_Name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Product name cannot be empty or just whitespace."
            )
        return value

    # Validate Price
    def validate_Price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value

    # Validate Description
    def validate_Description(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Description cannot be empty or just whitespace."
            )
        if len(value) < 10:
            raise serializers.ValidationError(
                "Description must be at least 10 characters long."
            )
        return value

    # Validate Brand
    def validate_Brand(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Brand cannot be empty or just whitespace."
            )
        return value

    # Validate Stock
    def validate_Stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative.")
        return value

    # Validate Ingredients
    def validate_Ingredients(self, value):
        if not isinstance(value, list):
            raise serializers.ValidationError("Ingredients must be a list.")
        return value

    # Validate Category
    def validate_Category(self, value):
        if value not in ["Cat", "Dog"]:
            raise serializers.ValidationError("Category must be either 'Cat' or 'Dog'.")
        return value

    # Override the create method to upload image to S3
    def create(self, validated_data):
        image_file = validated_data.get('Image')
    
        if image_file:
        # Generate a unique name for the image, and use it as the file name in S3
            image_name = f'products/{image_file.name}'  # 'products/' is the folder where you want to store images in S3
        # Use your utility function to upload the image to S3
            image_url = upload_image_to_s3(image_file, image_name)
            if not image_url:
                raise serializers.ValidationError("Image upload failed.")
        # Store the S3 URL in the Image field
            validated_data['Image'] = image_url

        return super().create(validated_data)
    

    
