from django.contrib import admin
from .models import Clothing, Categories, Color, Size, ProductImages, Temptable

# Register your models here.
admin.site.register(Clothing)
admin.site.register(Categories)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(ProductImages)
admin.site.register(Temptable)