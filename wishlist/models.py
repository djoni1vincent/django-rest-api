from django.db import models

from products.models import Product
from users.models import CustomUser

# Create your models here.


class Wishlist(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["user"]
