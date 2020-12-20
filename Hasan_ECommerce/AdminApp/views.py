from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.core.files.storage import default_storage
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

    template_name = 'AdminApp/all_product.html'

    def post(self, request, *args, **kwargs):

        product_ids = request.POST.getlist("p_ids")
        product_qtys = request.POST.getlist("p_qty")
        product_prices = request.POST.getlist("p_price");
        print(product_ids)
        print(product_qtys)
        print(product_prices)

        for index in range(len(product_ids)):
            # extracting the updated values
            p_id = product_ids[index]
            p_qty = product_qtys[index]
            p_price = product_prices[index]

            if p_qty != '' and p_price != '' and p_id != '':
                product = Clothing.objects.filter(id=p_id).update(price=p_price, quantity=p_qty)

        return redirect('admin_app:ad_all_prods')


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

    def post(self, request, *args, **kwargs):

        p_id = self.kwargs["id"]
        table = request.POST["t_name"]
        attr = request.POST["p_attr"]
        print(p_id, table, attr)
        cloth_instance = Clothing.objects.get(id=p_id)

        if table == "f7bd60":

            product_attr = Size.objects.create(id=cloth_instance.id, name=attr)

        elif table == "70dda5":

            p_code = request.POST["p_attr_code"]
            product_attr = Color.objects.create(id=p_id, name=attr, code=p_code)

        return redirect(f'/0baea2/admin/products/{p_id}')

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


def DeleteProductAttrs(request, id, table, attr):

    if table == "f7bd60":

        product_attr = Size.objects.filter(id=id, name=attr).delete()

    elif table == "70dda5":

        product_attr = Color.objects.filter(id=id, name=attr).delete()

    return redirect(f'/0baea2/admin/products/{id}')


class AddNewProduct(TemplateView):

    template_name = 'AdminApp/add_product.html'

    def post(self, request, *args, **kwargs):

        p_name = request.POST["p_name"]
        p_desc = request.POST["p_desc"]
        p_price = request.POST["p_price"]
        p_qty = request.POST["p_qty"]
        p_gender = request.POST.getlist("p_gender")[0]
        p_cat = request.POST.getlist("p_category")[0]

        insert_product = Clothing.objects.create(
            brand_name = "Hasan Co.",
            product_name = p_name,
            product_desc = p_desc,
            price = p_price,
            gender = p_gender,
            category = p_cat,
            quantity = p_qty 
        )

        p_id = insert_product.id

        files = request.FILES.getlist('p_imgs')

        for i, img in enumerate(files):

            #  adding a suffix to the p_id starting with 1 i.e., 1006_1.
            temp_id = str(p_id) + f'_{i+1}'
            instance = ProductImages.objects.create(id=p_id, name=img, temp=temp_id)

        return redirect('admin_app:ad_new_prod')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_woman'] = result[1]
        context['username'] = result[2]

        return context

    
def DeleteProduct(request, id):

    delete_product = Clothing.objects.filter(id=id).delete()

    delete_p_sizes = Size.objects.filter(id=id).delete()
    delete_p_colors = Color.objects.filter(id=id).delete()

    # Retrieving all the Images of the product, and deleting them.
    p_images = ProductImages.objects.filter(id=id)
    for img in p_images:
        path = str(img.name)
        print(path)
        if default_storage.exists(path):
            default_storage.delete(path)

    p_images = ProductImages.objects.filter(id=id).delete()

    return redirect('admin_app:ad_all_prods')