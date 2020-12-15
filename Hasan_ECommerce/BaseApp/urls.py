from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    IndexView,
    ProductsView,
    ProductsByCategory,
    ProductDesc,
    AddToCart,
    Cart,
    Update_Quantity
)

app_name = 'base_app'

urlpatterns = [
    path('cart/', login_required(Cart.as_view()), name="cart"),
    path('u_qty/<str:opr>/<int:cloth_id>/', Update_Quantity, name="update_quantity"),
    path('add_to_cart/<str:pg>/<int:id>/<str:mrp>/<str:gender>/<str:category>/', AddToCart, name="add_to_cart"),
    path('<str:type>/', ProductsView.as_view(), name="product"),
    path('<str:type>/<str:category>/', ProductsByCategory.as_view()),
    path('<str:type>/<str:category>/<int:id>/', ProductDesc.as_view()),
]