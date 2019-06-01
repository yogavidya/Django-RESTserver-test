"""Oauth2_test URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, re_path, include
from django.contrib.auth.views import LoginView
from .views import oauth2_get_token
from .apis import UserListCreate, UserDestroy

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    path('login/', LoginView.as_view(template_name='login.html')),
    path('access', oauth2_get_token),
    path('users', UserListCreate.as_view()),
    #re_path(r'^users/delete/([0-9]{1,10})', UserDestroy.as_view()),
    path('users/delete/<pk>', UserDestroy.as_view()),
]
