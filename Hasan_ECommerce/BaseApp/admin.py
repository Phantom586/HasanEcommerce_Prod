from django.contrib import admin
from .models import Clothing, Categories, Color, Size, ProductImages, InvoiceTable, BasketTable, UserTable

# Register your models here.
admin.site.register(Clothing)
admin.site.register(Categories)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductImages)
admin.site.register(InvoiceTable)
admin.site.register(BasketTable)
admin.site.register(UserTable)