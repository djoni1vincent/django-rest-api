from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r"posts", views.PostsViewSet, basename="posts")
router.register(r"read_only", views.PostReadOnlyViewSet, basename="read_only")

urlpatterns = [
    path("", include(router.urls)),
]
