from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    AllProducts, ProductDetails
)

app_name = "admin_app"

urlpatterns = [
    path('', AllProducts.as_view(), name="us-admin"),
    path('products/<int:id>/', ProductDetails.as_view()),
]