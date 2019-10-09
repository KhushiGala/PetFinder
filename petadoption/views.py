from django.shortcuts import render
from .forms import UserRegisterForm, PetRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser, Pet


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
# def user_login(request):
#     if request.method == 'POST':
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             print('form is valid')
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             user = authenticate(username=username, password=password)
#             if user:
#                 print('user exists')
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('explore'))
#             else:
#                 print('user does not exist')
#                 messages.error(request, 'Incorrect Credentials')
#                 print("Someone tried to login and failed.")
#                 print("They used username: {} and password: {}".format(username,password))
#
#         return render(request,'login.html',{'form':form})
#     else:
#         form = UserLoginForm()
#         return render(request, 'login.html', {'form':form})
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                messages.success(request, 'You have logged in successfully')
                return HttpResponseRedirect(reverse('explore'))
            else:
                return HttpResponse("Your account was inactive.")
            login(request,user)
            return HttpResponseRedirect(reverse('explore'))
        else:
            #print("Someone tried to login and failed.")
            #print("They used username: {} and password: {}".format(username,password))
            messages.error(request,'Invalid Login Details!')
            #template="reservation/login.html"
            #return HttpResponse("Invalid Details")
    return render(request, 'login.html')

def explore(request):
    return render(request, 'explore.html')

@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'You have logged out successfully')
    return HttpResponseRedirect(reverse('user_login'))



@login_required
def pet_register(request):
    if request.method == 'POST':
        pet_form = PetRegisterForm(request.POST, request.FILES)
        if pet_form.is_valid:
            mypet = pet_form.save(commit=False)
            mypet.owner = request.user
            mypet.save()
            messages.success(request, 'Pet Successfully Added')
            return HttpResponseRedirect(reverse('explore'))
        else:
            messages.error(request, 'Incorrect details')
            #return render(request, 'SignUp.html',{'form':form})

    else:
        pet_form = PetRegisterForm()
    return render(request, 'petregister.html',{'form':pet_form})


def user_register(request):
    #registration = False
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        if user_form.is_valid():
            # user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            username = user_form.cleaned_data['username']
            user = MyUser()
            try:
                user = MyUser.objects.get(username=username)
                messages.error(request, 'Username exists')
                return render(request,'SignUp.html',{'form':form})
            except user.DoesNotExist:
                # if user is None:
                #user_form.save(commit=True)
                my_user = user_form.save(commit=False)
                my_user.set_password(user_form.cleaned_data['password'])
                my_user.save()
                #registration=True
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
