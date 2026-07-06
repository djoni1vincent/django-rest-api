from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer
from users.serializers import UserSerializer

from .models import Wishlist


class WishlistSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    products = ProductSerializer(many=True, read_only=True)
    products_ids = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), many=True, write_only=True, source="products"
    )

    class Meta:
        model = Wishlist
        fields = ["id", "user", "products", "products_ids", "created_at"]
