from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    IndexView, ProductsView, ProductsByCategory,
    ProductDesc, AddToCart, Cart, Update_Quantity,
    Checkout, Confirmation, ForgotPassword,
    ResetPassword
)

app_name = 'base_app'

urlpatterns = [
    path('cart/', login_required(Cart.as_view()), name="cart"),
    path('checkout/', login_required(Checkout.as_view()), name="checkout"),
    path('confirmation/', login_required(Confirmation.as_view()), name="confirm"),
    path('forgot_password/', login_required(ForgotPassword.as_view()), name="forgot-pass"),
    path('reset_password/', login_required(ResetPassword.as_view()), name="reset-pass"),
    path('u_qty/<str:opr>/<int:cloth_id>/', Update_Quantity, name="update_quantity"),
    path('add_to_cart/<str:pg>/<int:id>/<str:mrp>/<str:gender>/<str:category>/', AddToCart, name="add_to_cart"),
    path('products/<str:type>/', ProductsView.as_view(), name="product"),
    path('products/<str:type>/<str:category>/', ProductsByCategory.as_view()),
    path('products/<str:type>/<str:category>/<int:id>/', ProductDesc.as_view()),
]