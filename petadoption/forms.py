from django import forms
from django.contrib.admin import widgets
from .models import MyUser

# class UserRegisterForm(forms.ModelForm):
#     first_name=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style", 'type':"text", 'placeholder':"First Name", 'name':"first_name"}))
#     last_name=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style", 'type':"text", 'placeholder':"Last Name", 'name':"last_name"}))
#     username = forms.CharField(widget=forms.TextInput(attrs={'class':"input--style-3", 'type':"text" , 'placeholder':"Username",'name':"username"}))
#     password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"input--style-3", 'type':"password" ,'placeholder':"Password" ,'name':"password"}))
#     email=forms.EmailField(widget=forms.EmailInput(attrs={'class':"input--style-3", 'type':"email" ,'placeholder':"Email" ,'name':"email"}))
#     class Meta():
#         model = MyUser
#         fields = ('username','first_name','last_name','password','email')
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'type':"password" ,'name':"password"}))
    class Meta():
        model = MyUser
        fields = ['username','email','first_name','last_name']


class UserLoginForm(forms.ModelForm):
    #username = forms.CharField(widget=forms.TextInput(attrs={'class':"input--style-3", 'type':"text" , 'placeholder':"Username",'name':"username"}))
    #password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"input--style-3", 'type':"password" ,'placeholder':"Password" ,'name':"password"}))
    class Meta():
        model = MyUser
        fields = ['username', 'password']

# from django import forms
# from django.contrib.admin import widgets
# from .models import MyUser
# from django.contrib.auth.forms import UserCreationForm, UserChangeForm
#
# class UserRegisterForm(UserCreationForm):
#     #first_name=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style", 'type':"text", 'placeholder':"First Name", 'name':"first_name"}))
#     #last_name=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style", 'type':"text", 'placeholder':"Last Name", 'name':"last_name"}))
#     #username=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style-3", 'type':"text" ,'placeholder':"Username" ,'name':"username"}))
#     #password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"input--style-3", 'type':"password" ,'placeholder':"Password" ,'name':"password"}))
#     #email=forms.EmailField(widget=forms.EmailInput(attrs={'class':"input--style-3", 'type':"email" ,'placeholder':"Email" ,'name':"email"}))
#     class Meta():
#         model = MyUser
#         fields = ('username', 'password')
#         #fields = ('first_name','last_name','username','password','email')
# # class CustomUserCreationForm(UserCreationForm):
# #
# #     class Meta:
# #         model = CustomUser
# #         fields = ('username', 'email')
#
# # class CustomUserChangeForm(UserChangeForm):
# #
# #     class Meta:
# #         model = CustomUser
# #         fields = ('username', 'email')
