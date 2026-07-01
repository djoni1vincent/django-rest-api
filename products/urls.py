from django.urls import include, path
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"reviews", views.ReviewViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
