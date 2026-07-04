"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)

from users.views import CustomTokenObtainPairView

urlpatterns = [
    path("admin/", admin.site.urls),
    path(
        "api/schema/v1/", SpectacularAPIView.as_view(api_version="v1"), name="schema-v1"
    ),
    path(
        "api/schema/v2/", SpectacularAPIView.as_view(api_version="v2"), name="schema-v2"
    ),
    path("", RedirectView.as_view(url="/api/schema/v1/swagger-ui/")),
    path("api/<str:version>/", include("products.urls")),
    # auth
    path("api/token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "api/schema/v1/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema-v1"),
        name="swagger-v1-ui",
    ),
    path(
        "api/schema/v2/swagger-ui/",
        SpectacularSwaggerView.as_view(url_name="schema-v2"),
        name="swagger-v2-ui",
    ),
    path("silk/", include("silk.urls", namespace="silk")),
]
