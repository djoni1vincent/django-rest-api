from rest_framework import status
from rest_framework.test import APITestCase

from users.models import CustomUser

from .models import Category, Product, Review

# Create your tests here.


class ProductTests(APITestCase):
    model = Product

    def setUp(self):
        self.regular_user = CustomUser.objects.create_user(
            username="regular",
            email="regular@example.com",
            password="password",
        )
        self.staff_user = CustomUser.objects.create_user(
            username="staff",
            email="staff@example.com",
            password="password",
            is_staff=True,
        )

        self.category = Category.objects.create(name="Test", slug="test")

    def test_anonymous_can_list_products(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_anonymous_can_not_create_products(self):
        response = self.client.post("/products/", data={})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_regular_can_not_create_products(self):
        self.client.force_authenticate(user=self.regular_user)
        response = self.client.post(
            "/products/",
            data={
                "name": "Test Product",
                "price": "10.00",
                "description": "Test Description",
                "category_ids": [self.category.id],
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_staff_can_create_products(self):
        self.client.force_authenticate(user=self.staff_user)
        response = self.client.post(
            "/products/",
            data={
                "name": "Test Product",
                "price": "10.00",
                "description": "Test Description",
                "category_ids": [self.category.id],
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_author_can_delete_own_review(self):
        self.client.force_authenticate(user=self.staff_user)
        product = Product.objects.create(
            name="Test Product",
            price="10.00",
            description="Test Description",
        )

        product.category.add(self.category)

        review = Review.objects.create(
            product=product, author=self.staff_user, comment="Test Review", rating=5
        )

        response = self.client.delete(f"/reviews/{review.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_another_user_can_not_delete_review(self):
        self.client.force_authenticate(user=self.regular_user)

        product = Product.objects.create(
            name="Test Product",
            price="10.00",
            description="Test Description",
        )

        product.category.add(self.category)

        review = Review.objects.create(
            product=product, author=self.staff_user, comment="Test Review", rating=5
        )
        response = self.client.delete(f"/reviews/{review.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
