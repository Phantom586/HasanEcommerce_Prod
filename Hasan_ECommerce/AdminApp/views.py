from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from BaseApp.models import (
    Clothing, Categories, Color, Size, 
    ProductImages, InvoiceTable, BasketTable,
    UserTable
)


def get_nav_categories(u_id, logged_in=False):

    category_men = list(Categories.objects.filter(gender="men"))
    category_woman = list(Categories.objects.filter(gender="woman"))

    u_name = ""

    if logged_in:
        user = UserTable.objects.get(id=u_id)
        u_name = user.name

    return [category_men, category_woman, u_name]


class AllProducts(TemplateView):

    template_name = 'AdminApp/all_products.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        products_list = list(Clothing.objects.all())

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]
        context['products_list'] = products_list

        return context

class ProductDetails(TemplateView):

    template_name = 'AdminApp/prod_details.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_id = self.kwargs["id"]

        p_details = Clothing.objects.get(id=p_id)
        p_colors = Color.objects.filter(id=p_id)
        p_size = Size.objects.filter(id=p_id)
        p_images = ProductImages.objects.filter(id=p_id)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]
        context['product_details'] = p_details
        context['colors'] = p_colors
        context['sizes'] = p_size
        context['images'] = p_images

        return context