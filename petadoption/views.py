from django.shortcuts import render
from .forms import UserRegisterForm

# Create your views here.
def home_page(request):
    return render(request,'explore.html',{})
def user_register(request):
    registration = False
    if request.method == 'POST':
        form = UserRegisterForm(data=request.POST)
        if form.is_valid():
            a = "abc"
    else:
        return render(request, '')
# def login_user(request):
#     if request.method=='POST':
#             user_form =
