from django.contrib import admin
from django.urls import include, path

from accounts.views import JWKSView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/auth/", include("accounts.urls")),
    path(".well-known/jwks.json", JWKSView.as_view(), name="jwks"),
]
