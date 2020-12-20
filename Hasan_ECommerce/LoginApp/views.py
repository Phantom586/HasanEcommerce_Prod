from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib import messages
from BaseApp.models import Categories, UserTable

# Create your views here.
def get_nav_categories():

    category_men = list(Categories.objects.filter(gender="men"))
    category_woman = list(Categories.objects.filter(gender="woman"))

    return [category_men, category_woman]


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
        context['categories_woman'] = result[1]

    return render(request, 'LoginApp/register.html', {'form':form, 'data' :context})


def Login(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('hasan-home')
        else:
            messages.warning(request, "Entered username or password is incorrect.")
            return redirect('login')

    result = get_nav_categories()

    context = {}

    context['categories_men'] = result[0]
    context['categories_woman'] = result[1]

    return render(request, 'LoginApp/login.html', {'data':context})


def Logout(request):

    logout(request)

    return redirect('login')