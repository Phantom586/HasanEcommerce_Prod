from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    AllProducts, ProductDetails, DeleteProductAttrs,
    AddNewProduct, DeleteProduct, DeleteProductImages,
    AddCategory,DeleteCategory
)

app_name = "admin_app"

urlpatterns = [
    path('', AllProducts.as_view(), name="ad_all_prods"),
    path('delete/<int:id>/', DeleteProduct, name="ad_delete_prod"),
    path('delete_imgs/<int:id>/', DeleteProductImages, name="delete_prod_imgs"),
    path('add_product/', AddNewProduct.as_view(), name="ad_new_prod"),
    path('add_category/', AddCategory.as_view(), name="ad_new_cat"),
    path('add_category/delete/<str:gender>/<str:name>/', DeleteCategory, name="delete_category"),
    path('products/<int:id>/', ProductDetails.as_view()),
    path('products/<int:id>/<str:table>/<str:attr>/', DeleteProductAttrs),
]