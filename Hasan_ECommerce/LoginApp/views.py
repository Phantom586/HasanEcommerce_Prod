from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib import messages
from django.views.generic import TemplateView
from BaseApp.models import Categories, UserTable
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
import uuid

# Create your views here.
def get_nav_categories():

    category_men = list(Categories.objects.filter(gender="men"))
    category_women = list(Categories.objects.filter(gender="women"))

    return [category_men, category_women]


def Register(request):
    
    context = {}

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            
            form.save()
            
            full_name = form.cleaned_data.get('full_name')
            email = form.cleaned_data.get('email')
            phone_no = form.cleaned_data.get('phone_no')

            new_user = UserTable.objects.create(
                name = full_name,
                phone_no = phone_no,
                email = email
            )

            return redirect('login')

    else:

        form = UserRegisterForm()

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]

    return render(request, 'LoginApp/register.html', {'form':form, 'data' :context})


def Login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # Setting the Session_ID for the current Session.
            request.session['Sess_ID'] = str(uuid.uuid4().hex)
            return redirect('hasan-home')
        else:
            messages.warning(request, "Entered username or password is incorrect.")
            return redirect('login')

    result = get_nav_categories()

    context = {}

    context['categories_men'] = result[0]
    context['categories_women'] = result[1]

    return render(request, 'LoginApp/login.html', {'data':context})


def Logout(request):

    logout(request)

    return redirect('login')


class ForgotPassword(TemplateView):

    template_name  = 'LoginApp/forgotPass.html'

    def post(self, request, *args, **kwargs):

        if request.method == "POST":

            email = request.POST["email"]
            phone_no = request.POST["phone"]
            print(email, phone_no)

            user_exists = UserTable.objects.filter(phone_no=phone_no, email=email).count()
            print(user_exists)
            
            user = UserTable.objects.get(phone_no=phone_no, email=email)

            if user_exists > 0:
                return redirect(f'/reset_password/{user.id}')
            else:
                messages.warning(request, 'You\'ve Entered  Invalid Email or Phone No.')
                return redirect('/forgot_password/')

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]

        return context


class ResetPassword(TemplateView):

    template_name  = 'LoginApp/resetPass.html'

    def post(self, request, *args, **kwargs):

        password = request.POST["first_pass"]
        conf_pass = request.POST["sec_pass"]
        u_id = self.kwargs["id"]

        if password == conf_pass:
            # Validating the entered pass with in-built validator.
            try:
                is_valid = validate_password(conf_pass)
                if is_valid is None:
                    # Retrieving the user from User Model.
                    user = User.objects.get(id=u_id)
                    user.set_password(conf_pass)
                    user.save()
                    # Logging in the user.
                    login(request, user)
                    return redirect('login')
            except ValidationError as ve:
                for warning in ve:
                    messages.warning(request, warning)
                return redirect(f'/reset_password/{u_id}')
        else:
            messages.warning(request, 'Entered passwords don\'t match.')
            return redirect(f'/reset_password/{u_id}')


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        result = get_nav_categories()

        context['categories_men'] = result[0]
        context['categories_women'] = result[1]

        return context