from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
def register(request):

    if request.method == "POST":

        form = UserRegisterForm(request.POST)

        if form.is_valid():
            form.save()
            
            u_name = form.cleaned_data.get('username')

            messages.success(request, f'Account Created for {u_name}!')

            return redirect('login')

    else:

        form = UserRegisterForm()

    return render(request, 'LoginApp/register.html', {'form':form})

