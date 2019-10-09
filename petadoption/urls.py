from django.contrib import admin
from django.urls import path,include,re_path
from . import views

urlpatterns = [
path('register/', views.pet_register, name='pet_register'),
]
