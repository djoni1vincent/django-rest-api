from django.urls import include, path
from django.views.generic import RedirectView
from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register(r"products", views.ProductViewSet)
router.register(r"categories", views.CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
