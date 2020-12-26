from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.db.models import F, Sum
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.mail import send_mail
import uuid
from .models import (
    Clothing, Categories, Color, Size, 
    ProductImages, InvoiceTable, BasketTable,
    UserTable, TempBasket
)

shipping_charge = 50

def get_nav_categories(u_id, logged_in=False):

    category_men = list(Categories.objects.filter(gender="men"))
    category_woman = list(Categories.objects.filter(gender="women"))

    u_name = ""

    if logged_in:
        user = UserTable.objects.get(id=u_id)
        u_name = user.name

    return [category_men, category_woman, u_name]



class IndexView(TemplateView):
    
    template_name = 'BaseApp/index.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect('hasan-home')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]

        return context


class ProductsView(TemplateView):

    template_name = 'BaseApp/products.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect(f'/home/products/{self.kwargs["type"]}')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        p_type = self.kwargs['type']

        clothes_list = list(Clothing.objects.filter(gender=p_type).values())
    
        clothes_count = Clothing.objects.filter(gender=p_type).values().count()
        
        category_list = list(Categories.objects.filter(gender=p_type))

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]

        context['products'] = clothes_list
        context['categories'] = category_list
        context['type'] = p_type
        context['Type'] = p_type.title()
        context['count'] = clothes_count

        return context


class ProductsByCategory(TemplateView):

    template_name = 'BaseApp/products.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect(f'/home/products/{self.kwargs["type"]}/{self.kwargs["category"]}')

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
        context['categories_women'] = result[1]
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

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect(f'/home/products/{self.kwargs["type"]}/{self.kwargs["category"]}/{self.kwargs["id"]}')

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
        context['categories_women'] = result[1]
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
    context['categories_women'] = result[1]
    context['username'] = result[2]

    p_size = request.GET["p_size"]
    p_color = request.GET["p_color"]
    p_qty = request.GET["p_qty"]
    sess_id = request.session['Sess_ID']

    # Checking if the product doesn't already exists in the DB.
    exists = TempBasket.objects.filter(user_id=user_id, cloth_id=id, size=p_size, color=p_color).count()

    if exists > 0:
        update_prod = TempBasket.objects.filter(user_id=user_id, cloth_id=id, size=p_size, color=p_color).update(quantity=F('quantity')+1, total_mrp=F('mrp')*F('quantity'))
    else :
        t_mrp = int(p_qty) * int(mrp)
        store_in_basket = TempBasket.objects.create(
            user_id = user_id,
            cloth_id = id,
            session_id = sess_id,
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
    
    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect('base_app:cart')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        products_list = list(TempBasket.objects.filter(user_id=u_id).values())
        total_amount = TempBasket.objects.filter(user_id=u_id).aggregate(Sum('total_mrp'))
        total_amount = total_amount['total_mrp__sum']

        for product in products_list:
            cloth_id = product['cloth_id']
            cloth = Clothing.objects.get(id=cloth_id)
            product['name'] = cloth.product_name

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]
        context['total_amount'] = total_amount
        context['products_list'] = products_list

        return context
    

def Update_Quantity(request, opr, cloth_id):

    u_id = request.user.id

    if opr == "8c3642":
        update_prod = TempBasket.objects.filter(user_id=u_id, cloth_id=cloth_id).update(quantity=F('quantity')+1, total_mrp=F('mrp')*F('quantity'))
    elif opr == "fc05f9":
        # Checking if the qty. of the product is >= 0 or not.
        cloth_details = TempBasket.objects.get(user_id=u_id, cloth_id=cloth_id)
        p_qty = cloth_details.quantity

        if p_qty > 1:
            update_prod = TempBasket.objects.filter(user_id=u_id, cloth_id=cloth_id).update(quantity=F('quantity')-1, total_mrp=F('mrp')*F('quantity'))
        else:
            # Deleting the Record.
            TempBasket.objects.filter(user_id=u_id, cloth_id=cloth_id).delete()

    return redirect('/home/cart')


class Checkout(TemplateView):

    template_name = 'BaseApp/checkout.html'

    def post(self, request, *args, **kwargs):

        if request.method == "POST":

            search_str = request.POST["search_txt"]

            if search_str != "pseudo_search":

                return redirect(f'/search_results/{search_str}')

            addr = request.POST["addr"]
            city = request.POST["city"]
            pincode = request.POST["zip"]

            user = UserTable.objects.filter(id=request.user.id).update(address=addr, city=city, pincode=pincode)

            # generating txn_id and order_id
            txn_id = str(uuid.uuid4().hex)
            order_id = str(uuid.uuid4().hex)
            u_id = request.user.id
            total_mrp= TempBasket.objects.filter(user_id=u_id).aggregate(Sum('total_mrp'))
            total_mrp = total_mrp['total_mrp__sum']
            # adding shipping charge to total_mrp
            total_mrp = int(total_mrp) + shipping_charge
            sess_id = request.session["Sess_ID"]

            # storing the order in InvoiceTable.
            create_order = InvoiceTable.objects.create(
                session_id = sess_id,
                txn_id = txn_id,
                order_id = order_id,
                payment_mode = "Online",
                user = u_id,
                total_mrp = total_mrp
            )

            order_id = create_order.receipt_no
            invoice = InvoiceTable.objects.get(receipt_no=order_id)
            order_time = invoice.timestamp.strftime("%b %d, %Y  %I:%M %p")

            user= UserTable.objects.get(id=request.user.id)
            user_email = user.email

            # moving the products to be purchased to BasketTable.
            products_list = list(TempBasket.objects.filter(user_id=u_id).values())

            # var to hold the products bought, and details.
            html_data = f'<h3>This Order has been placed on {order_time}.</h3>\n<h4>Address : {user.address}</h4>\n'
            html_data += f'<h5>City : {user.city}</h5>\n<h5>Pincode : {user.pincode}</h5>\n'

            for i, product in enumerate(products_list):

                cloth_id = product['cloth_id']
                cloth = Clothing.objects.get(id=cloth_id)

                html_data += f"""
                <p>{i+1}. Product Name : {cloth.product_name} | Size : {product['size']} | Color : {product['color']}</p>
                    <p>Product Price : ₹{product['mrp']} | Quantity : x {product['quantity']} | Total Price : ₹{product['total_mrp']}</p>
                """

                store_in_basket = BasketTable.objects.create(
                    user_id = product['user_id'],
                    cloth_id = product['cloth_id'],
                    session_id = product['session_id'],
                    quantity = product['quantity'],
                    mrp = product['mrp'],
                    size = product['size'],
                    color = product['color'],
                    total_mrp = product['total_mrp']
                )

            html_data += f"""<p>Final Price : <strong>₹{total_mrp}</strong></p>"""

            # Sending mail  to the Site owner.
            response = send_mail(
                subject = f'Order #{order_id}',
                message = f'{user.name} has placed an order.',
                from_email = 'Hasanstorecms@gmail.com',
                # recipient_list = ['Rabshanh@gmail.com'],
                recipient_list = ['586pboy@gmail.com'],
                fail_silently=False,
                html_message = html_data,
            )

            print(f'Email Response : {response}')

            # Removing all the User's products from the TempBasket.
            remove_prods = TempBasket.objects.filter(user_id=u_id).delete()

            # resetting the session_id from session.
            request.session['Sess_ID'] = str(uuid.uuid4().hex)

            return redirect(f'/home/confirmation/{order_id}')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        products_list = list(TempBasket.objects.filter(user_id=u_id).values())
        total_amount = TempBasket.objects.filter(user_id=u_id).aggregate(Sum('total_mrp'))
        total_amount = total_amount['total_mrp__sum']

        for product in products_list:
            cloth_id = product['cloth_id']
            cloth = Clothing.objects.get(id=cloth_id)
            product['name'] = cloth.product_name

        # User's Delivery Address values
        addr = ""
        city = ""
        pincode = ""

        user = UserTable.objects.get(id=u_id)
        if user.address:
            addr = user.address
        if user.city:
            city = user.city
        if user.pincode:
            pincode = user.pincode

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]
        context['total_amount'] = total_amount
        context['final_amt'] = total_amount + shipping_charge
        context['products_list'] = products_list
        context['address'] = addr
        context['city'] = city
        context['pincode'] = pincode

        return context


class Confirmation(TemplateView):

    template_name = 'BaseApp/confirm.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect(f'/home/confirmation/{self.kwargs["order_id"]}')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id
        order_id = self.kwargs['order_id']

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        user = UserTable.objects.get(id=u_id)
        
        invoice = InvoiceTable.objects.get(receipt_no=order_id)
        order_time = invoice.timestamp.strftime("%b %d, %Y  %I:%M %p")
        sess_id = invoice.session_id

        products_list = list(BasketTable.objects.filter(user_id=u_id, session_id=sess_id).values())
        total_amount = BasketTable.objects.filter(user_id=u_id, session_id=sess_id).aggregate(Sum('total_mrp'))
        total_amount = total_amount['total_mrp__sum']

        for product in products_list:
            cloth_id = product['cloth_id']
            cloth = Clothing.objects.get(id=cloth_id)
            product['name'] = cloth.product_name

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]
        context['total_amount'] = total_amount
        context['products_list'] = products_list
        context['ordered_on'] = order_time
        context['invoice'] = invoice
        context['s_user'] = user

        return context


class NewCollection(TemplateView):

    template_name = 'BaseApp/new_collection.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect(f'/new-collection/{self.kwargs["type"]}')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        p_type = self.kwargs["type"]

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        latest_prods = []

        if p_type == "all":
            latest_prods = list(Clothing.objects.all().order_by('-timestamp')[:10])
        elif p_type == "men" or p_type == "women":
            latest_prods = list(Clothing.objects.filter(gender=p_type).order_by('-timestamp')[:10])
        print(latest_prods)
        
        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]
        context['latest_prods'] = latest_prods

        return context


class Orders(TemplateView):

    template_name = 'BaseApp/orders.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST["search_txt"]

        if search_str != "":
            return redirect(f'/search_results/{search_str}')

        else:
            return redirect('base_app:orders')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)
        
        user = UserTable.objects.get(id=u_id)

        # Fetching the Orders by latest Orders first.
        Invoices = list(InvoiceTable.objects.filter(user=u_id).values().order_by('-timestamp'))

        for invoice in Invoices:
            sess_id = invoice['session_id']
            # Retrieving the products purchased in this order.
            products_list = list(BasketTable.objects.filter(user_id=u_id, session_id=sess_id).values())
            for product in products_list:
                cloth_id = product['cloth_id']
                cloth = Clothing.objects.get(id=cloth_id)
                product['name'] = cloth.product_name
            total_amount = BasketTable.objects.filter(user_id=u_id, session_id=sess_id).aggregate(Sum('total_mrp'))
            total_amount = total_amount['total_mrp__sum']
            order_time = invoice['timestamp'].strftime("%b %d, %Y  %I:%M %p")
            invoice['products_list'] = products_list
            invoice['subtotal'] = total_amount
            invoice['order_time'] = order_time

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]
        context['invoices'] = Invoices
        context['s_user'] = user

        return context


class SearchResults(TemplateView):

    template_name  = 'BaseApp/search_results.html'

    def post(self, request, *args, **kwargs):

        search_str = request.POST['search_txt']

        return redirect(f'/search_results/{search_str}')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        u_id = self.request.user.id

        logged_in = self.request.user.is_authenticated

        result = get_nav_categories(u_id, logged_in)

        search_str = self.kwargs['search_str']

        results = list(Clothing.objects.filter(product_name__icontains=search_str).values())
        print(results)

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]
        context['username'] = result[2]
        context['products'] = results
        context['search_str'] = search_str

        return context