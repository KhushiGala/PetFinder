from django.shortcuts import render
from .forms import UserRegisterForm, PetRegisterForm, CommentForm, AdoptionRequestForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser, Pet, Comments, Adoption_requests



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


@login_required
def pet_info(request, pet_id):
    if request.method == 'POST':
        if 'comment_form_submit' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid:
                mycomment = comment_form.save(commit=False)
                mycomment.comment_writer = request.user
                mycomment.pet_id = Pet.objects.filter(id=pet_id)[0]
                mycomment.save()
        else:
            adoption_form = AdoptionRequestForm(request.POST)
            if adoption_form.is_valid:
                myadoptionrequest = adoption_form.save(commit=False)
                myadoptionrequest.pet = Pet.objects.filter(id=pet_id)[0]
                myadoptionrequest.requester = request.user
                myadoptionrequest.save()
    new_comment_form = CommentForm()
    new_adoption_form = AdoptionRequestForm()
    mypet = Pet.objects.get(id=pet_id)
    comments = Comments.objects.filter(pet_id=pet_id).order_by('created')
    comments_count = comments.count()
    return render(request, 'blog-single.html', {'pet':mypet, 'comments_count':comments_count, 'comments':comments, 'comment_form':new_comment_form, 'adoption_form':new_adoption_form, 'delete_pet':delete_pet})

@login_required
def myaccount(request, user_username, pet_id):
    user = MyUser.objects.filter(username=user_username)[0]
    pet_list = Pet.objects.filter(owner=user)
    if pet_id=='0':
        pet_selected = False
        adoption_request_list = Adoption_requests.objects.none()
    else:
        pet_selected = True
        adoption_request_list = Adoption_requests.objects.filter(pet=pet_id).order_by('created')
    # for p in pet_list:
    #     instance = Adoption_requests.objects.filter(pet=p)
    #     adoption_request_list = adoption_request_list.union(instance)
    return render(request, 'myaccount.html', context={'pet_list':pet_list , 'adoption_list':adoption_request_list, 'pet_selected':pet_selected })

@login_required
def explore(request):
    pet_list = Pet.objects.order_by('?')[:16]
    #pet_list = Pet.objects.filter(up_for_adoption='Y').order_by('?')[:16]
    return render(request, 'explore.html', context={'pet_list':pet_list})


@login_required
def adoption_explore(request):
    pet_list = Pet.objects.filter(up_for_adoption='Y').order_by('?')[:16]
    return render(request, 'adoption_explore.html', context={'pet_list':pet_list})


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
    if request.method == 'POST':
        user_form = UserRegisterForm(data=request.POST)
        if user_form.is_valid():
            username = user_form.cleaned_data['username']
            user = MyUser()
            try:
                user = MyUser.objects.get(username=username)
                messages.error(request, 'Username exists')
                return render(request,'SignUp.html',{'form':user_form})
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
        else:
            messages.error(request, 'Incorrect details')
            return render(request, 'SignUp.html',{'form':user_form})

    else:
        form = UserRegisterForm()
        return render(request, 'SignUp.html',{'form':form})

def user_logout(request):
   logout(request)
   return HttpResponseRedirect(reverse('user_login'))

def delete_pet(request, pet_id):
    query = Pet.objects.get(id=pet_id)
    query.delete()
    messages.success(request, 'You have Deleted successfully')
    return HttpResponseRedirect(reverse('explore'))


def about(request):
    return render(request, 'about.html')
