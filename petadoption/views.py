from django.shortcuts import render
from .forms import UserRegisterForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser


# Create your views here.
# def home_page(request):
#     return render(request,'explore.html',{})

# def user_login(request):
#     if request.method == 'GET':
#         form = LoginForm()
#         return render(request, 'login.html', {'form':form})
#     else:
#         #u = request.
#         form = LoginForm(request.POST)
#         #if form.is_valid():
#         #username = form.cleaned_data['username']
#         #password = form.cleaned_data['password']
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = authenticate(username=username, password=password)
#         if user:
#             print('User {} logged in successfully'.format(username))
#             login(request, user)
#             return HttpResponseRedirect(reverse('explore'))
#         else:
#             print(username,password)
#             print('Login Username:{}  Password:{} failed'.format(username, password))
#     return HttpResponseRedirect(reverse('user_login'))
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('explore'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            message="Invalid Login Details !"
            check=True
            template="reservation/login.html"
            return HttpResponse("Invalid Details")
    else:
        return render(request, 'login.html', {})

def explore(request):
    return render(request, 'explore.html')


def user_register(request):
    registration = False
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            username = form.cleaned_data['username']
            user = MyUser()
            try:
                user = MyUser.objects.get(username=username)
                messages.error(request, 'Username exists')
                return render(request,'SignUp.html',{'form':form})
            except user.DoesNotExist:
                # if user is None:
                form.save(commit=True)
                registration=True
                messages.success(request, 'Successfully Registered')
                messages.success(request, 'Please Log In to Continue')
                return HttpResponseRedirect(reverse('user_login'))
            # else:
                # messages.error(request, 'Username exists')
                # return render(request,'SignUp.html',{'form':form})
        else:
            messages.error(request, 'Incorrect details')
            return render(request, 'SignUp.html',{'form':form})

    else:
        form = UserRegisterForm()
        return render(request, 'SignUp.html',{'form':form})
# def login_user(request):
#     if request.method=='POST':
#             user_form =
