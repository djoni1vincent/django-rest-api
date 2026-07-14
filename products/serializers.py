from rest_framework import serializers

from users.serializers import UserSerializer

from .models import Category, Product, Review


# test
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True, source="category"
    )
    price = serializers.DecimalField(
        max_digits=10, decimal_places=2, source="price_amount"
    )
    help_text = "The price of the product in the format {amount} {currency}"

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "category_ids",
            "description",
        ]


class ProductV2Serializer(serializers.ModelSerializer):
    category = CategorySerializer(many=True, read_only=True)
    category_ids = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True, write_only=True, source="category"
    )
    price = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "category_ids",
            "price",
            "description",
        ]

    def get_price(self, obj):
        return {
            "amount": obj.price_amount,
            "currency": obj.price_currency,
        }


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
