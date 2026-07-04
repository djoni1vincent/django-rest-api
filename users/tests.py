from rest_framework.test import APITestCase

from .models import CustomUser


# Create your tests here.
class LoginThrottleTests(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', password='testpassword')

    def test_login_throttle(self):
