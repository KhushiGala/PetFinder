from django.contrib import admin
from .models import Pet
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
#from .forms import CustomUserCreationForm, CustomUserChangeForm
from .forms import UserRegisterForm
from .models import MyUser

class MyUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    #form = CustomUserChangeForm
    model = MyUser
    list_display = ['password', 'username',]

admin.site.register(MyUser, MyUserAdmin)
