from django_filters.rest_framework import DjangoFilterBackend, FilterSet
from drf_spectacular.utils import extend_schema
from rest_framework import filters, viewsets
from rest_framework.permissions import AllowAny, IsAdminUser

from .models import Category, Product, Review
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    CategorySerializer,
    ProductSerializer,
    ProductV2Serializer,
    ReviewSerializer,
)


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "name": ["exact", "contains"],
            "category": ["exact"],
            # "price": ["exact", "lte", "gte"],
        }


@extend_schema(tags=["products"])
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.prefetch_related("category").all()
    # queryset = Product.objects.get("category").all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter

    search_fields = ["name", "category__name"]
    ordering_fields = ["name", "price_amount"]

    def get_serializer_class(self):
        if self.request.version == "v2":
            return ProductV2Serializer
        return ProductSerializer

    def get_permissions(self):
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]


@extend_schema(tags=["Categories"])
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

@extend_schema(tags=["Reviews"])
class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
