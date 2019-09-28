from django import forms
from django.contrib.admin import widgets
from django.contrib.auth.models import User

class UserRegisterForm(forms.ModelForm):
    first_name=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style", 'type':"text", 'placeholder':"First Name", 'name':"first_name"}))
    last_name=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style", 'type':"text", 'placeholder':"Last Name", 'name':"last_name"}))
    username=forms.CharField(widget=forms.TextInput(attrs={'class':"input--style-3", 'type':"text" ,'placeholder':"Username" ,'name':"username"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':"input--style-3", 'type':"password" ,'placeholder':"Password" ,'name':"password"}))
    email=forms.EmailField(widget=forms.EmailInput(attrs={'class':"input--style-3", 'type':"email" ,'placeholder':"Email" ,'name':"email"}))
    class Meta():
        model = User
        fields = ('first_name','last_name','username','password','email')
