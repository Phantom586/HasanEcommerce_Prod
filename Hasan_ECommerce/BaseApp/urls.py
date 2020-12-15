from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    IndexView,
    ProductsView,
    ProductsByCategory,
    ProductDesc,
    AddToCart,
    Cart,
)

app_name = 'base_app'

urlpatterns = [
    # path('', IndexView.as_view(), name="hasan-home"),
    # path('products/<str:type>/', ProductsView.as_view(), name="product"),
    # path('products/<str:type>/<str:category>/', ProductsByCategory.as_view()),
    # path('products/<str:type>/<str:category>/<int:id>/', ProductDesc.as_view()),
    path('cart/', login_required(Cart.as_view()), name="cart"),
    path('add_to_cart/<str:pg>/<int:id>/<str:mrp>/<str:gender>/<str:category>/', AddToCart, name="add_to_cart"),
    path('<str:type>/', ProductsView.as_view(), name="product"),
    path('<str:type>/<str:category>/', ProductsByCategory.as_view()),
    path('<str:type>/<str:category>/<int:id>/', ProductDesc.as_view()),
]