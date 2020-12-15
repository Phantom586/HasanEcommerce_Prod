from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Clothing, Categories, Color, Size, ProductImages, Temptable


def get_nav_categories():

    category_men = list(Categories.objects.filter(gender="men"))
    category_woman = list(Categories.objects.filter(gender="woman"))

    return [category_men, category_woman]


class IndexView(TemplateView):
    
    template_name = 'BaseApp/index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]

        return context


class ProductsView(TemplateView):

    template_name = 'BaseApp/products.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_type = self.kwargs['type']

        clothes_list = list(Clothing.objects.filter(gender=p_type).values())
    
        clothes_count = Clothing.objects.filter(gender=p_type).values().count()
        
        category_list = list(Categories.objects.filter(gender=p_type))

        for clothes in clothes_list:
            cloth_id = clothes['id']
            cloth_colors = list(Color.objects.filter(id=cloth_id))
            cloth_sizes = list(Size.objects.filter(id=cloth_id))
            # print(f'ID : {cloth_id}, cloth_colors : {cloth_colors}, cloth_sizes : {cloth_sizes}')
            clothes['colors'] = cloth_colors
            clothes['size'] = cloth_sizes
            # print(clothes)

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]

        context['products'] = clothes_list
        context['categories'] = category_list
        context['type'] = p_type
        context['Type'] = p_type.title()
        context['count'] = clothes_count

        return context


class ProductsByCategory(TemplateView):

    template_name = 'BaseApp/products.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_type = self.kwargs['type']
        p_cat = self.kwargs['category']

        clothes_list = list(Clothing.objects.filter(gender=p_type, category=p_cat).values())
    
        clothes_count = Clothing.objects.filter(gender=p_type, category=p_cat).values().count()
        
        category_list = list(Categories.objects.filter(gender=p_type))

        for clothes in clothes_list:
            cloth_id = clothes['id']
            cloth_colors = list(Color.objects.filter(id=cloth_id))
            cloth_sizes = list(Size.objects.filter(id=cloth_id))
            # print(f'ID : {cloth_id}, cloth_colors : {cloth_colors}, cloth_sizes : {cloth_sizes}')
            clothes['colors'] = cloth_colors
            clothes['size'] = cloth_sizes
            # print(clothes)
            
        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]

        context['products'] = clothes_list
        context['categories'] = category_list
        context['category'] = p_cat
        context['type'] = p_type
        context['Type'] = p_type.title()
        context['count'] = clothes_count

        return context


class ProductDesc(TemplateView):

    template_name = 'BaseApp/prod_details.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_type = self.kwargs['type']
        p_cat = self.kwargs['category']
        p_id = self.kwargs['id']

        p_details = Clothing.objects.get(id=p_id)
        p_colors = Color.objects.filter(id=p_id)
        p_size = Size.objects.filter(id=p_id)
        p_images = ProductImages.objects.filter(id=p_id)

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['product_details'] = p_details
        context['category'] = p_cat
        context['type'] = p_type.title()
        context['colors'] = p_colors
        context['sizes'] = p_size
        context['images'] = p_images

        return context
        

class AddToCart(TemplateView):

    template_name = 'BaseApp/cart.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_id = self.kwargs['id']

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]

        return context


class Cart(TemplateView):

    template_name = 'BaseApp/cart.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_id = self.kwargs['id']

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]

        return context
    