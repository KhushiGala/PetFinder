from django.shortcuts import render
from .forms import UserRegisterForm, PetRegisterForm, CommentForm, AdoptionRequestForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MyUser, Pet, Comments, Adoption_requests
from django.core.mail import send_mail
from django.conf import settings


email_from = settings.EMAIL_HOST_USER
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
                owner_email = MyUser.objects.get(username=myadoptionrequest.pet.owner.username).email
                requester_email = request.user.email
                subject_owner = 'Adoption Request for your pet'
                subject_receiver = 'Adoption Request made by you'
                owner_message = myadoptionrequest.pet.pet_name+' has been requested for adoption by '+request.user.first_name+'. Open the website to view adoption request now.'
                receiver_message = 'You have requested for the adoption of '+myadoptionrequest.pet.pet_name+'.'
                owner_receipent = [owner_email]
                receiver_receipent = [requester_email]
                send_mail(subject_owner, owner_message, email_from, owner_receipent)
                send_mail(subject_receiver, receiver_message, email_from, receiver_receipent)
    new_comment_form = CommentForm()
    new_adoption_form = AdoptionRequestForm()
    mypet = Pet.objects.get(id=pet_id)
    comments = Comments.objects.filter(pet_id=pet_id).order_by('created')
    comments_count = comments.count()
    return render(request, 'blog-single.html', {'pet':mypet, 'comments_count':comments_count, 'comments':comments, 'comment_form':new_comment_form, 'adoption_form':new_adoption_form})

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
    my_requests = Adoption_requests.objects.filter(requester=user).order_by('created')
    return render(request, 'myaccount.html', context={'pet_list':pet_list , 'adoption_list':adoption_request_list, 'my_requests':my_requests, 'pet_selected':pet_selected })

@login_required
def explore(request):
    query = request.GET.get("q")
    if query:
        pet_list = Pet.objects.all().filter(
            Q(pet_name__icontains=query)|
            Q(animal_type__icontains=query[0])|
            Q(breed__icontains=query)
            )[:16]
    else:
        pet_list = Pet.objects.all().order_by('?')
    return render(request, 'explore.html', context={'pet_list':pet_list})


# @login_required
# def adoption_explore(request):
#     pet_list = Pet.objects.filter(up_for_adoption='Y').exclude(owner=request.user).order_by('?')
#     query = request.GET.get("q")
#     gen = request.GET.get("gender")
#     ty = request.GET.get("type")
#     if query or 'gen' or 'type' :
#         pet_list = pet_list.filter(
#             Q(pet_name__icontains=query)|
#             Q(breed__icontains=query)
#             )
#     if gen:
#         pet_list = pet_list.filter(
#             Q(gender__icontains=gen[0])
#             )
#     if ty:
#         pet_list = pet_list.filter(
#             Q(animal_type__icontains=ty[0])
#             )
#     else:
#         pet_list = Pet.objects.filter(up_for_adoption='Y').exclude(owner=request.user).order_by('?')
#         messages.success(request, 'Pet not found')
#     return render(request, 'adoption_explore.html', context={'pet_list':pet_list})

@login_required
def adoption_explore(request):
    dog_enabled = bool(request.GET.get('dog_checkbox'))
    cat_enabled = bool(request.GET.get('cat_checkbox'))
    all_pets = Pet.objects.filter(up_for_adoption='Y').exclude(owner=request.user)
    pet_list= Pet.objects.none()
    query = request.GET.get("q")
    if query or 'dog_checkbox' in request.GET or 'cat_checkbox' in request.GET:
        if query:
            if 'dog_checkbox' in request.GET:
                pet_list |= all_pets.filter(Q(pet_name__icontains=query)|Q(breed__icontains=query),Q(animal_type=Pet.dog))
            elif 'cat_checkbox' in request.GET:
                pet_list |= all_pets.filter(Q(pet_name__icontains=query)|Q(breed__icontains=query),Q(animal_type=Pet.cat))
            else:
                pet_list |= all_pets.filter(Q(pet_name__icontains=query)|Q(breed__icontains=query))
        else:
            if 'dog_checkbox' in request.GET:
                pet_list |= all_pets.filter(Q(animal_type=Pet.dog))
            if 'cat_checkbox' in request.GET:
                pet_list |= all_pets.filter(Q(animal_type=Pet.cat))
    else:
        pet_list = all_pets
    # pet_list = pet_list.order_by('?')[:16]
    return render(request, 'adoption_explore.html', context={'pet_list':pet_list,'dog_enabled':dog_enabled, 'cat_enabled':cat_enabled})



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


# def email(request):
#     subject = 'Pet request received'
#     message = 'You have received a request for pet adoption'
#     email_from = settings.EMAIL_HOST_USER
#     receipient_list = ['']
#     send_mail(subject, message, email_from, receipient_list)
#     return HttpResponseRedirect(reverse('explore'))
