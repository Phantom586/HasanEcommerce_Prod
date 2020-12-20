"""Hasan_ECommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from BaseApp import views as base_views
from LoginApp import views as login_views
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('', base_views.IndexView.as_view(), name="hasan-home"),
    path('login/', login_views.Login, name="login"),
    path('home/', include('BaseApp.urls')),
    path('logout/', login_views.Logout, name="logout"),
    path('register/', login_views.Register, name="register"),
    path('forgot_password/', login_views.ForgotPassword.as_view(), name="forgot-pass"),
    path('reset_password/<int:id>/', login_views.ResetPassword.as_view(), name="reset-pass"),
    path('admin7ddb46/', admin.site.urls),
    path('0baea2/admin/', include('AdminApp.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
