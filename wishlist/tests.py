from rest_framework import status
from rest_framework.test import APITestCase

from products.models import Category, Product
from users.models import CustomUser
from wishlist.models import Wishlist

# Create your tests here.


class WishlistViewSetTest(APITestCase):
    model = Wishlist

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="regular",
            email="regular@example.com",
            password="password",
        )
        self.another_user = CustomUser.objects.create_user(
            username="another",
            email="another@example.com",
            password="password",
        )
        self.category = Category.objects.create(name="Test", slug="test")
        self.product = Product.objects.create(
            name="Test Product",
            price_amount="10.00",
            description="Test Description",
        )
        self.product.category.add(self.category)

        self.wishlist = Wishlist.objects.create(user=self.user)
        self.wishlist.products.add(self.product)

    def test_user_can_get_products_in_wishlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(
            "/api/v1/wishlist/",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_can_add_new_product_to_wishlist(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/api/v1/wishlist/add_product/",
            data={"product_id": self.product.id},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_another_user_can_not_see_others_wishlist(self):
        self.client.force_authenticate(user=self.another_user)
        response = self.client.get(f"/api/v1/wishlist/{self.wishlist.id}/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_anon_can_not_see_wishlist(self):
        response = self.client.get(f"/api/v1/wishlist/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
