from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import (
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


class IndexView(TemplateView):
    
    template_name = 'BaseApp/index.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]

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

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]

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
            
        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]

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

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]
        context['product_details'] = p_details
        context['category'] = p_cat
        context['type'] = p_type.title()
        context['colors'] = p_colors
        context['sizes'] = p_size
        context['images'] = p_images

        return context
        

@login_required
def AddToCart(request, pg, id, mrp, gender, category):

    user_id = request.user.id

    result = get_nav_categories(user_id)

    context = {}

    context['categories_men'] = result[0]
    context['categories_woman'] = result[1]
    context['username'] = result[2]

    p_size = request.GET["p_size"]
    p_color = request.GET["p_color"]
    p_qty = request.GET["p_qty"]

    # Checking if the product doesn't already exists in the DB.
    exists = BasketTable.objects.filter(user_id=user_id, cloth_id=id).count()

    if exists > 0:
        update_prod = BasketTable.objects.filter(user_id=user_id, cloth_id=id).update(quantity=F('quantity')+1, total_mrp=F('mrp')*F('quantity'))
    else :
        t_mrp = int(p_qty) * int(mrp)
        store_in_basket = BasketTable.objects.create(
            user_id = user_id,
            cloth_id = id,
            quantity = p_qty,
            mrp = mrp,
            size = p_size,
            color = p_color,
            total_mrp = t_mrp
        )

    redirect_link = ""

    if pg == "f5bf48":
        redirect_link = f'/home/products/{gender}/{category}'
    elif pg == "c0929b":
        redirect_link = f'/home/products/{gender}/{category}/{id}'

    return redirect( redirect_link)


class Cart(TemplateView):

    template_name = 'BaseApp/cart.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        products_list = list(BasketTable.objects.filter(user_id=u_id).values())
        total_amount = BasketTable.objects.filter(user_id=u_id).aggregate(Sum('total_mrp'))
        total_amount = total_amount['total_mrp__sum']

        for product in products_list:
            cloth_id = product['cloth_id']
            cloth = Clothing.objects.get(id=cloth_id)
            product['name'] = cloth.product_name

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]
        context['total_amount'] = total_amount
        context['products_list'] = products_list

        return context
    

def Update_Quantity(request, opr, cloth_id):

    u_id = request.user.id

    if opr == "8c3642":
        update_prod = BasketTable.objects.filter(user_id=u_id, cloth_id=cloth_id).update(quantity=F('quantity')+1, total_mrp=F('mrp')*F('quantity'))
    elif opr == "fc05f9":
        # Checking if the qty. of the product is >= 0 or not.
        cloth_details = BasketTable.objects.get(user_id=u_id, cloth_id=cloth_id)
        p_qty = cloth_details.quantity

        if p_qty > 1:
            update_prod = BasketTable.objects.filter(user_id=u_id, cloth_id=cloth_id).update(quantity=F('quantity')-1, total_mrp=F('mrp')*F('quantity'))
        else:
            # Deleting the Record.
            BasketTable.objects.filter(user_id=u_id, cloth_id=cloth_id).delete()

    return redirect('/home/cart')


class Checkout(TemplateView):

    template_name = 'BaseApp/checkout.html'

    def post(self, request, *args, **kwargs):

        if request.method == "POST":

            addr = request.POST["addr"]
            city = request.POST["city"]
            pincode = request.POST["zip"]
            print(addr, city, pincode)

            user = UserTable.objects.filter(id=request.user.id).update(address=addr, city=city, pincode=pincode)

            return render(request, 'BaseApp/confirm.html', {})

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        products_list = list(BasketTable.objects.filter(user_id=u_id).values())
        total_amount = BasketTable.objects.filter(user_id=u_id).aggregate(Sum('total_mrp'))
        total_amount = total_amount['total_mrp__sum']

        for product in products_list:
            cloth_id = product['cloth_id']
            cloth = Clothing.objects.get(id=cloth_id)
            product['name'] = cloth.product_name

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]
        context['total_amount'] = total_amount
        context['final_amt'] = total_amount + 50
        context['products_list'] = products_list

        return context


class Confirmation(TemplateView):

    template_name = 'BaseApp/confirm.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]

        return context
