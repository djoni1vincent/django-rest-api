from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Category, Product, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True, source="category"
    )

    class Meta:
        model = Product
        fields = ["id", "name", "category", "category_ids", "price", "description"]


class ReviewSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), write_only=True, source="product"
    )

    class Meta:
        model = Review
        fields = [
            "id",
            "product",
            "product_id",
            "author",
            "rating",
            "comment",
            "created_at",
        ]
        read_only_fields = ["id", "created_at", "author"]
