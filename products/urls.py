from django.urls import include, path
from rest_framework import routers

from . import views

product_router = routers.SimpleRouter()
product_router.register(r"products", views.ProductViewSet)

catalog_router = routers.SimpleRouter()
catalog_router.register(r"categories", views.CategoryViewSet)
catalog_router.register(r"reviews", views.ReviewViewSet)

# versioned: v1 (flat price) vs v2 ({amount, currency})
urlpatterns = [
    path("", include(product_router.urls)),
]

# v1-only: no v2 behavior exists for these
catalog_urlpatterns = [
    path("", include(catalog_router.urls)),
]
