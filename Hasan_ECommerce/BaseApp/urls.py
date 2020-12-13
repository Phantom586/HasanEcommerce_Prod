from django.urls import path, include
from .views import (
    IndexView,
    ProductsView,
    ProductsByCategory,
    ProductDesc
)

app_name = 'base_app'

urlpatterns = [
    path('', IndexView.as_view(), name="hasan-home"),
    path('products/<str:type>/', ProductsView.as_view(), name="product"),
    path('products/<str:type>/<str:category>/', ProductsByCategory.as_view()),
    path('products/<str:type>/<str:category>/<int:id>/', ProductDesc.as_view()),
]