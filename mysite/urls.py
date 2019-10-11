"""mysite URL Configuration

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
from django.urls import path,include,re_path
from petadoption import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    #path('admin/', admin.site.urls),
    #path('login/', views.login_user),
    #path('register/', views.user_register),
    path('', views.user_login, name='user_login'),
    path('sign_up/', views.user_register, name='user_register'),
    path('explore/', views.explore, name='explore'),
    path('pet/', include('petadoption.urls')),
    #path('myaccount/', views.my_account, name='my_account'),
    #path('pet/register/', views.pet_register, name='pet_register'),
    path('logout/', views.user_logout, name='user_logout'),
    path('admin/', admin.site.urls)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
